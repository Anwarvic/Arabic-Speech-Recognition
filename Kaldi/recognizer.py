import os
from glob import glob
from tqdm import tqdm

from kaldi.asr import GmmLatticeFasterRecognizer
from kaldi.decoder import LatticeFasterDecoderOptions
from kaldi.feat.mfcc import Mfcc, MfccOptions
from kaldi.feat.functions import compute_deltas, DeltaFeaturesOptions
from kaldi.feat.window import FrameExtractionOptions
from kaldi.transform.cmvn import Cmvn
from kaldi.util.table import SequentialMatrixReader, SequentialWaveReader

class Recognizer():

    def __init__(self, model_dir, model_name):
        """
        This method is used define the class member variables.
        Parameters:
            - model_dir (string): full path where the trained models are located
            - model_name (string): the name of the model.
               Kaldi uses these names by convention:
                * mono         * tri1         * tri2
        This method sets these member variables:
            - MODEL_DIR: same as model_dir
            - MODEL_NAME: same as model_name
            - ASR: The actual speech recognition object
        """
        self.MODEL_DIR = model_dir
        self.MODEL_NAME = model_name
        #set decoding options (same as archive/config/decode.conf)
        decoder_opts = LatticeFasterDecoderOptions()
        decoder_opts.beam = 13.0
        decoder_opts.lattice_beam = 6.0
        # decoder_opts.max_active = 7000
        # Construct recognizer
        self.ASR = GmmLatticeFasterRecognizer.from_files(
            os.path.join(self.MODEL_DIR, self.MODEL_NAME, "final.mdl"),
            os.path.join(self.MODEL_DIR, self.MODEL_NAME, "graph", "HCLG.fst"),
            os.path.join(self.MODEL_DIR, self.MODEL_NAME, "graph", "words.txt"),
            decoder_opts=decoder_opts)

    
    def __create_transcription(self, data_path):
        """
        This private method is used to create a text transcription file
        that contain the files name that need to be decoded
        Parameters:
            - data_path (string): full path of the data directory containing
              wav files to be decoded, or just a wav-file.
        Usage:
        >>> create_transcription("/home/desktop/recoreded_data)
        or
        >>> create_transcription("home/desktop/recorded_data/01.wav")
        NOTE:
        Any non-wav file existing in data_path will be neglected!!
        """
        assert os.path.exists(data_path), "provided a valid path"
        #check wether data_path is a directory or just one file
        if os.path.isdir(data_path):
           wav_files = sorted(glob(os.path.join(data_path, "*.wav")))
           if len(wav_files) == 0:
               wav_files = sorted(glob(os.path.join(data_path, "*", "*.wav"), recursive=True))
        else:
            wav_files = [data_path]
        with open("wav.scp", "w") as fout:
            for wav_path in wav_files:
                _, wav_filename = os.path.split(wav_path)
                wav_filename = wav_filename[:-4] #remove extension
                fout.write("{} {}\n".format(wav_filename, wav_path))
                

    # Define feature pipeline in code
    def __make_feat_pipeline(self, base, opts=DeltaFeaturesOptions()):
        """
        This private method is used to create a feature pipeline.
        Parameters:
            - base (kaldi.feat.mfcc object): #TODO
            - opts: #TODO
        Returns:
            - It returns a function that represents pipeline of a wav
        """
        def feat_pipeline(wav):
            feats = base.compute_features(wav.data()[0], wav.samp_freq, 1.0)
            cmvn = Cmvn(base.dim())
            cmvn.accumulate(feats)
            cmvn.apply(feats)
            return compute_deltas(opts, feats)
        return feat_pipeline


    def decode(self, data_path, remove_scp=True):
        """
        This method is used to decode a wav file/directory.
        Parameters:
            - data_path (string): full path of the data directory containing
              wav files to be decoded, or just a wav-file.
            - remove_scp (bool): remove transcription file wav.scp that is created
              for decoding.
        Returns:
            - accuracy (int): The accuracy of the the model over these wav files.
            (In case of wav.scp contains just one file)
            - Returns the true word & predicted word
            (In case of wav.scp contains more than one file)
            - model_decoded (csv file): It also returns a csv file where a more detailed
              results about the decoding process can be found!!
        """
        #create transcription file
        self.__create_transcription(data_path)
        #down-sample wav file
        frame_opts = FrameExtractionOptions()
        frame_opts.samp_freq = 16000
        frame_opts.allow_downsample = True
        #mfcc features (same as archive/config/mfcc.conf)
        mfcc_opts = MfccOptions()
        mfcc_opts.use_energy = False
        mfcc_opts.frame_opts = frame_opts
        #create pipeline
        pipeline = self.__make_feat_pipeline(Mfcc(mfcc_opts))
        
        #words of the data
        WORDS = ["صفر", "واحد", "إثنان", "ثلاثة", "أربعة", "خمسة",
                 "ستة", "سبعة", "ثمانية", "تسعة", "التنشيط", "التحويل",
                 "الرصيد", "التسديد", "نعم", "لا", "التمويل", "البيانات",
                 "الحساب", "إنهاء"]
        #start decoding
        correct = 0.
        with open("wav.scp", "r") as fin:
            num_wavs = len(fin.readlines())
        
        with open("{}_decoding.csv".format(self.MODEL_NAME), 'w') as fout:
            #write csv header
            fout.write("{},{},{},{}\n".format("Filename", "TrueWord", "Predicted", "Likelihood"))
            #iterate over wav files
            for key, wav in tqdm(SequentialWaveReader("scp:wav.scp"), total=num_wavs, desc="Decoding"):
                true_word_id = int(key.split(".")[-1])-1
                true_word = WORDS[true_word_id]
                feats = pipeline(wav)
                out = self.ASR.decode(feats)
                if num_wavs > 1:
                    fout.write("{},{},{},{}\n".format(key, true_word, out["text"], out["likelihood"]))
                #was it correct??
                if true_word == out["text"]:
                    correct+=1.
            if num_wavs == 1:
                print("TrueWord:", true_word)
                print("PredictedWord:", out["text"])
                print("Likelihood:", out["likelihood"])
        #remove wav.scp
        os.remove("wav.scp")
        return correct/num_wavs



if __name__ == "__main__":
    #create model
    model_dir = "/media/anwar/E/ASR/Kaldi/kaldi/egs/arabic_corpus_of_isolated_words/exp"
    model_name = "tri1"
    rec = Recognizer(model_dir, model_name)
    
    #decode
    path = "/media/anwar/D/Data/ASR/IST-Dataset_mono/Anwar"
    score = rec.decode(path, remove_scp=True)
    print("Accuracy: {}%".format(score*100))
