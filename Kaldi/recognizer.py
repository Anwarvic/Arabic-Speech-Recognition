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
                * tri3a        * tri4a
        This method sets these member variables:
            - MODEL_DIR: same as model_dir
            - MODEL_NAME: same as model_name
            - ASR: The actual speech recognition object
        """
        self.MODEL_DIR = model_dir
        self.MODEL_NAME = model_name
        # Construct recognizer
        decoder_opts = LatticeFasterDecoderOptions()
        decoder_opts.beam = 11.0
        decoder_opts.max_active = 7000
        self.ASR = GmmLatticeFasterRecognizer.from_files(
            os.path.join(self.MODEL_DIR, self.MODEL_NAME, "final.mdl"),
            os.path.join(self.MODEL_DIR, self.MODEL_NAME, "graph", "HCLG.fst"),
            os.path.join(self.MODEL_DIR, self.MODEL_NAME, "graph", "words.txt"),
            decoder_opts=decoder_opts)

    
    def create_transcription(self, data_dir):
        """
        This method is used to create a text transcription file that contain 
        the files name that need to be decoded
        Parameters:
            - data_dir (string): full path of the data directory.
        
        NOTE: Any non-wav file existing in data_dir will be neglected!!
        """
        pass


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


    def decode(self, wav_trans="wav.scp"):
        """
        This method is used to decode a wav file/directory.
        Parameters:
            - wav_trans (string): the filename of the trainscription of the wav(s) that
              need(s) to be decoded.
        Returns:
            - accuracy (int): The accuracy of the the model over these wav files.
            - model_decoded (csv file): It also returns a csv file where a more detailed
              results about the decoding process can be found!!
        """
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
                fout.write("{},{},{},{}\n".format(key, true_word, out["text"], out["likelihood"]))
                # print(key, out["text"], flush=True)
                #was it correct??
                if true_word == out["text"]:
                    correct+=1.
        return correct/num_wavs


if __name__ == "__main__":
    model_dir = "/media/anwar/E/ASR/Kaldi/kaldi/egs/arabic_corpus_of_isolated_words/exp"
    model_name = "tri1"
    rec = Recognizer(model_dir, model_name)
    print("Accuracy: {}%".format(rec.decode()*100))
