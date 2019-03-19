import os
import re
import random
import shutil
from glob import glob
from tqdm import tqdm


def safe_makedir(dirname):
    """
    Creates a directory recursively if not existed
    """
    if not os.path.exists(dirname):
        os.makedirs(dirname)


class DataOrganizer():

    def __init__(self):
        # name of the dataset that will be used at kaldi
        self.DATASET = "arabic_corpus_of_isolated_words"
        self.INDIR = "/media/anwar/D/Data/ASR/Arabic_Corpus_of_Isolated_Words"
        self.OUTDIR = os.path.join("/media/anwar/E/ASR/Kaldi/kaldi/egs", self.DATASET)
        safe_makedir(self.OUTDIR)
        
        self.EXCLUDE_SPEAKERS_IDS = {11, 36, 44}
        self.TRAIN_SPEAKERS, self.TEST_SPEAKERS = self.__splitSpeakers(ratio=0.8)
        self.EXCLUDE_WORDS_IDS = set([])
        self.TRAIN_WAVFILES, self.TEST_WAVFILES = self.__getAudioFiles()
        self.WORDS = ["صفر", "واحد", "إثنان", "ثلاثة", "أربعة", "خمسة",
                      "ستة", "سبعة", "ثمانية", "تسعة", "التنشيط", "التحويل",
                      "الرصيد", "التسديد", "نعم", "لا", "التمويل", "البيانات",
                      "الحساب", "إنهاء"]


    def __splitSpeakers(self, ratio=0.8):
        """
        This function is used to split the speaker IDs to two sets
        (enroll, test) basted on the given ration after filtering some
        IDs which are defined inside EXCLUDED_IDS which are the female.
        
        NOTE: The number of speakers in the Arabic Corpus of Isolated Words
        are 50 whose IDs vary from [1-50]
        """
        assert ratio >=0 and ratio <=1,\
            "ratio is a ratio number between [0, 1] inclusively"
        random.seed(0)
        #IDs from 1 to 50
        total_ids = set(range(1, 51))
        #exclude the EXCLUDED_IDS
        remaining_ids = list(total_ids - self.EXCLUDE_SPEAKERS_IDS)
        #shuffle
        random.shuffle(remaining_ids)
        #split based on the ratio
        split = int(len(remaining_ids)*ratio)
        train_ids = remaining_ids[:split] 
        test_ids = remaining_ids[split:]
        return ["S"+str(i).zfill(2) for i in train_ids], ["S"+str(i).zfill(2) for i in test_ids]


    def __getAudioFiles(self):
        """
        This method is used to get all the audio files that maps to the
        WORD_IDS after excluding EXCLUDE_SPEAKERS

        NOTE: The number of words in the Arabic Corpus of Isolated Words
        is 20 whose IDs vary from [1-20]
        """
        #IDs from 1 to 20
        total_ids = set(range(1, 21))
        #exclude the EXCLUDED_IDS
        remaining_word_ids = list(total_ids - self.EXCLUDE_WORDS_IDS)
        train_wavFiles = []
        test_wavFiles = []
        for sp in self.TRAIN_SPEAKERS:
            for word_id in remaining_word_ids:
                file_regex = sp+".*."+str(word_id).zfill(2)+".wav" #get files from 
                train_wavFiles.extend(glob(os.path.join(self.INDIR, sp, file_regex)))
        train_wavFiles = [os.path.split(wav)[-1] for wav in train_wavFiles]
        for sp in self.TEST_SPEAKERS:
            for word_id in remaining_word_ids:
                file_regex = sp+".*."+str(word_id).zfill(2)+".wav" #get files from 
                test_wavFiles.extend(glob(os.path.join(self.INDIR, sp, file_regex)))
        test_wavFiles = [os.path.split(wav)[-1] for wav in test_wavFiles]
        return train_wavFiles, test_wavFiles


    def prepare_audio(self):
        """
        This method is used to prepare the "Arabic Corpus of Isolated Words" data
        for Kaldi. It should locate the preprocessed data inside "kaldi/egs/DATASET"
        where DATASET is the name of your dataset
        """
        #create data directory
        safe_makedir(os.path.join(self.OUTDIR, "data"))
        #create train directory
        train_dir = os.path.join(self.OUTDIR, "data", "train")
        safe_makedir(train_dir)
        # Copy training wav files
        for filename in tqdm(self.TRAIN_WAVFILES, desc="Copying Train dataset"):
            speaker, rep, wordId, ext = filename.split(".")
            #create speaker directory
            safe_makedir(os.path.join(train_dir, speaker))
            filepath = os.path.join(self.INDIR, speaker, filename)
            newFilepath = os.path.join(train_dir, speaker, filename)
            #copy the file
            shutil.copyfile(filepath, newFilepath)
        #create test directory
        test_dir = os.path.join(self.OUTDIR, "data", "test")
        safe_makedir(test_dir)
        # Copy training wav files
        for filename in tqdm(self.TEST_WAVFILES, desc="Copying Test dataset"):
            speaker, rep, wordId, ext = filename.split(".")
            #create speaker directory
            safe_makedir(os.path.join(test_dir, speaker))
            filepath = os.path.join(self.INDIR, speaker, filename)
            newFilepath = os.path.join(test_dir, speaker, filename)
            #copy the file
            shutil.copyfile(filepath, newFilepath)


    def create_spk2gender(self):
        """
        This method is used to create spk2gender file that maps the 
        speakers to their gender following this pattern
        <speaker_id> <gender>
        According to the gender, it's either 'm' for male or
        'f' for female.
        NOTE: all speakers are male
        """
        train_dir = os.path.join(self.OUTDIR, "data", "train")
        with open(os.path.join(train_dir, "spk2gender"), "w") as fout:
            for speaker in os.listdir(train_dir):
                if os.path.isdir(os.path.join(train_dir, speaker)):
                    fout.write("{} {}\n".format(speaker, "m"))

        test_dir = os.path.join(self.OUTDIR, "data", "test")
        with open(os.path.join(test_dir, "spk2gender"), "w") as fout:
            for speaker in os.listdir(test_dir):
                if os.path.isdir(os.path.join(test_dir, speaker)):
                    fout.write("{} {}\n".format(speaker, "m"))


    def create_wav_scp(self):
        """
        This method is used to create "wav.scp" file that maps the
        utterance id to the audio wav file. utterance id is a name
        that is unique for each audio file in the data
        """
        train_dir = os.path.join(self.OUTDIR, "data", "train")
        with open(os.path.join(train_dir, "wav.scp"), "w") as fout:
            for speaker in os.listdir(train_dir):
                if os.path.isdir(os.path.join(train_dir, speaker)):
                    for wav_file in sorted(os.listdir(os.path.join(train_dir, speaker))):
                        absPath = os.path.join(train_dir, wav_file)
                        fout.write("{}_{} {}\n".format(speaker, wav_file[:-4], absPath))

        test_dir = os.path.join(self.OUTDIR, "data", "test")
        with open(os.path.join(test_dir, "wav.scp"), "w") as fout:
            for speaker in os.listdir(test_dir):
                if os.path.isdir(os.path.join(test_dir, speaker)):
                    for wav_file in sorted(os.listdir(os.path.join(test_dir, speaker))):
                        absPath = os.path.join(test_dir, wav_file)
                        fout.write("{}_{} {}\n".format(speaker, wav_file[:-4], absPath))


    def create_text(self):
        """
        This method is used to create "text" file that maps the
        utterance id to the text. It follows this pattern
        <utterance id> <text>
        """
        train_dir = os.path.join(self.OUTDIR, "data", "train")
        with open(os.path.join(train_dir, "text"), "w") as fout:
            for speaker in os.listdir(train_dir):
                if os.path.isdir(os.path.join(train_dir, speaker)):
                    for wav_file in sorted(os.listdir(os.path.join(train_dir, speaker))):
                        speaker, rep, wordId, ext = wav_file.split(".")
                        fout.write("{}_{} {}\n".format(speaker, wav_file[:-4], self.WORDS[int(wordId)]))

        test_dir = os.path.join(self.OUTDIR, "data", "test")
        with open(os.path.join(test_dir, "text"), "w") as fout:
            for speaker in os.listdir(test_dir):
                if os.path.isdir(os.path.join(test_dir, speaker)):
                    for wav_file in sorted(os.listdir(os.path.join(test_dir, speaker))):
                        speaker, rep, wordId, ext = wav_file.split(".")
                        fout.write("{}_{} {}\n".format(speaker, wav_file[:-4], self.WORDS[int(wordId)]))

    def create_utt2spk(self):
        """
        This method is used to create utt2spk file that maps the 
        utterances ids to their speaker following this pattern
        <utterance_id> <speaker>
        """
        train_dir = os.path.join(self.OUTDIR, "data", "train")
        with open(os.path.join(train_dir, "utt2spk"), "w") as fout:
            for speaker in os.listdir(train_dir):
                if os.path.isdir(os.path.join(train_dir, speaker)):
                    for wav_file in sorted(os.listdir(os.path.join(train_dir, speaker))):
                        fout.write("{}_{} {}\n".format(speaker, wav_file[:-4], speaker))

        test_dir = os.path.join(self.OUTDIR, "data", "test")
        with open(os.path.join(test_dir, "utt2spk"), "w") as fout:
            for speaker in os.listdir(test_dir):
                if os.path.isdir(os.path.join(test_dir, speaker)):
                    for wav_file in sorted(os.listdir(os.path.join(test_dir, speaker))):
                        speaker, rep, wordId, ext = wav_file.split(".")
                        fout.write("{}_{} {}\n".format(speaker, wav_file[:-4], speaker))


    # def create_local_text():
    #     """
    #     This method is used to create the text file exists
    #     in the local directory. This file should contain 
    #     all the sentences used in the audio files.
    #     This file should contain every sentence in a
    #     separate line
    #     """
    def prepare_mapping_files(self):
        """
        This method is used to prepare the mapping files
        that connects (speakers, audio data, gender, text)
        to each other. These files are used by Kaldi.

        This method reads audio data used by Kaldi, so if their a
        """
        train_dir = os.path.join(self.OUTDIR, "data", "train")
        test_dir = os.path.join(self.OUTDIR, "data", "test")
        assert os.path.exists(train_dir) and os.path.exists(test_dir),\
            "Audio data can't be found. Run prepare_audio() method first"

        #prepare speaker to gender (spk2geder) mapping file





if __name__ == "__main__":
    obj = DataOrganizer()
    # obj.prepare_audio()
    # obj.create_spk2gender()
    # obj.create_wav_scp()
    # obj.create_text()
    # obj.create_utt2spk()
    obj.local_text()
