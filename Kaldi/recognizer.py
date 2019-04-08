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

    def __init__(self, base_dir, model_name, kaldi_dir):
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
        self.BASE_DIR = base_dir
        self.MODEL_NAME = model_name.lower()
        #TODO: assert here
        self.MODEL_DIR = os.path.join(self.BASE_DIR, "exp", self.MODEL_NAME)
        self.KALDI_DIR = kaldi_dir
        self.ASR = self.__initialize_decoder()

        
    def __initialize_decoder(self):
        # if self.MODEL_NAME in ["mono", "tri1", "tri2"]:
        #set decoding options (same as archive/config/decode.conf)
        decoder_opts = LatticeFasterDecoderOptions()
        decoder_opts.beam = 13.0
        decoder_opts.lattice_beam = 6.0
        # decoder_opts.max_active = 7000
        
        # Construct recognizer
        asr = GmmLatticeFasterRecognizer.from_files(
                os.path.join(self.MODEL_DIR, "final.mdl"),
                os.path.join(self.MODEL_DIR, "graph", "HCLG.fst"),
                os.path.join(self.MODEL_DIR, "graph", "words.txt"),
                decoder_opts=decoder_opts)
        # else:
        #     pass
        return asr

    
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
    def __make_feat_pipeline(self):
        """
        This private method is used to create a feature pipeline based on the model.
        The pipeline is divided into two parts:
        -> pre-processing:
            - Computing MFCC features using compute-mfcc-feats binary file
              over mfcc.conf file and wav transcription file
            - Normalize the extracted features using apply-cmvn-sliding binary file
        -> processing:
            this part differs between a model to the other
        Returns:
            - a string that represents unix-like pipeline of the feature extraction process
        
        RESOURCES:
        http://kaldi-asr.org/doc/io.html#io_sec_specifiers_both
        """
        # define the rspecifier for reading the features
        if self.MODEL_NAME in ["mono", "tri1", "tri2"]:
            feats_rspecifier = (
                "ark,s,cs:"
                #does the same functionality as archive/steps/make_mfcc.sh
                "{0}/src/featbin/compute-mfcc-feats --allow-downsample --config=archive/conf/mfcc.conf scp:wav.scp ark:-"
                #does the same functionality as archive/steps/compute_cmvn_stats.sh
                #NOTE: we have set the cmn-window so big to normalize over the whole audio file
                " | {0}/src/featbin/apply-cmvn-sliding --cmn-window=1000000000 --center=true ark:- ark:-"
                #does the same functionality found at archive/steps/train_mono.sh and archive/steps/train_deltas.sh
                " | {0}/src/featbin/add-deltas ark:- ark:-"
                " |".format(self.KALDI_DIR)
            )
        elif self.MODEL_NAME in ["tri3a", "tri4a"]:
            feats_rspecifier = (
                 "ark,s,cs:"
                 #does the same functionality as archive/steps/make_mfcc.sh
                "{0}/src/featbin/compute-mfcc-feats --allow-downsample --config=archive/conf/mfcc.conf scp:wav.scp ark:-"
                #does the same functionality as archive/steps/compute_cmvn_stats.sh
                #NOTE: we have set the cmn-window so big to normalize over the whole audio file
                " | {0}/src/featbin/apply-cmvn-sliding --cmn-window=1000000000 --center=true ark:- ark:-"
                #the next two commands do the same functionality found at archive/steps/train_lda_mllt.sh 
                #and archive/steps/train_sat.sh
                " | {0}/src/featbin/splice-feats ark:- ark:-"
                " | {0}/src/featbin/transform-feats {1}/final.mat ark:- ark:-"
                " |".format(self.KALDI_DIR, self.MODEL_DIR)
            )
        
        # print(feats_rspecifier)
        return feats_rspecifier


    def evaluate(self, data_path, remove_scp=True):
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
        #create pipeline
        pipeline = self.__make_feat_pipeline()
        #words of the data
        WORDS = ["صفر", "واحد", "إثنان", "ثلاثة", "أربعة", "خمسة",
                 "ستة", "سبعة", "ثمانية", "تسعة", "التنشيط", "التحويل",
                 "الرصيد", "التسديد", "نعم", "لا", "التمويل", "البيانات",
                 "الحساب", "إنهاء"]
        #start decoding
        with open("wav.scp", "r") as fin:
            num_wavs = len(fin.readlines())
        
        with open("{}_decoding.csv".format(self.MODEL_NAME), 'w') as fout:
            #write csv header
            fout.write("{},{},{},{}\n".format("Filename", "TrueWord", "Predicted", "Likelihood"))
            correct = 0.
            #iterate over wav features
            for key, feats in SequentialMatrixReader(pipeline):
                true_word_id = int(key.split(".")[-1])-1
                true_word = WORDS[true_word_id]
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
        # os.remove("wav.scp")
        return correct/num_wavs



if __name__ == "__main__":
    #create model
    base_dir = "/media/anwar/E/ASR/Kaldi/kaldi/egs/arabic_corpus_of_isolated_words"
    model_name = "tri3a"
    kaldi_dir = "/media/anwar/E/ASR/Kaldi/kaldi"
    rec = Recognizer(base_dir, model_name, kaldi_dir)
    
    #decode
    path = "/media/anwar/D/Data/ASR/IST-Dataset_mono/Remon/S01.01.01.wav"
    score = rec.evaluate(path, remove_scp=True)
    print("Accuracy: {}%".format(score*100))
