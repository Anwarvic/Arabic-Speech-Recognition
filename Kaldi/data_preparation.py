import os
import re
import shutil
import subprocess
from glob import glob
from tqdm import tqdm
from distutils.dir_util import copy_tree
from utils import *



class DataOrganizer():

    def __init__(self):
        #name of the dataset in kaldi (TODO: You can Modify this)
        self.dataset = "ist"
        #absolute path of the data (TODO: You MUST Modify this)
        self.indir = "/media/anwar/D/Data/ASR/Arabic_Corpus_of_Isolated_Words"
        #absolute path of the our processed data in kaldi (TODO: You MUST Change this)
        self.basedir = "/media/anwar/E/ASR/Kaldi/kaldi/egs" #it must be inside kaldi/egs
        
        #set constant directories
        self.OUTDIR = os.path.join(self.basedir, self.dataset)
        self.TRAIN_DIR = os.path.join(self.OUTDIR, "data", "train")
        self.TEST_DIR = os.path.join(self.OUTDIR, "data", "test")
        safe_makedir(self.OUTDIR)
        
        #words of the data
        self.WORDS = ["صفر", "واحد", "إثنان", "ثلاثة", "أربعة", "خمسة",
                      "ستة", "سبعة", "ثمانية", "تسعة", "التنشيط", "التحويل",
                      "الرصيد", "التسديد", "نعم", "لا", "التمويل", "البيانات",
                      "الحساب", "إنهاء"]
        # exclude words by id (wordId is the index of the word in self.WORDS)
        self.EXCLUDE_WORDS_IDS = set([])
        
        self.FEMALE_SPEAKERS_IDS = {11, 36, 44}
        self.MALE_SPEAKERS_IDS = set(range(1, 51)) - self.FEMALE_SPEAKERS_IDS
        self.EXCLUDE_SPEAKERS_IDS = self.FEMALE_SPEAKERS_IDS
        self.TRAIN_SPEAKERS, self.TEST_SPEAKERS = self.__splitSpeakers(ratio=0.8)


    def __splitSpeakers(self, ratio=0.8):
        """
        This private method is used to split the speakers into two sets
        (train, test) basted on the given ratio after filtering some
        IDs which are defined inside EXCLUDE_WORDS_IDS.
        NOTE: The number of speakers in the "Arabic Corpus of Isolated Words"
        dataset are 50 whose IDs vary from [1-50].
        """
        assert ratio >=0 and ratio <=1,\
            "ratio is a ratio number between [0, 1] inclusively"
        import random
        random.seed(0)
        #IDs from 1 to 50
        total_ids = set(range(1, 51))
        #exclude some speakers found in EXCLUDE_SPEAKERS_IDS
        remaining_ids = list(total_ids - self.EXCLUDE_SPEAKERS_IDS)
        #shuffle
        random.shuffle(remaining_ids)
        #split based on the ratio
        split = int(len(remaining_ids)*ratio)
        train_ids = remaining_ids[:split] 
        test_ids = remaining_ids[split:]
        return  ["S"+str(i).zfill(2) for i in train_ids], \
                ["S"+str(i).zfill(2) for i in test_ids]


    def __getAudioFiles(self):
        """
        This method is used to get all the audio files of the TRAIN_SPEAKERS and 
        TEST_SPEAKERS that maps to WORDS after excluding EXCLUDE_WORDS_IDS
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
                train_wavFiles.extend(glob(os.path.join(self.indir, sp, file_regex)))
        train_wavFiles = [os.path.split(wav)[-1] for wav in train_wavFiles]
        for sp in self.TEST_SPEAKERS:
            for word_id in remaining_word_ids:
                file_regex = sp+".*."+str(word_id).zfill(2)+".wav" #get files from 
                test_wavFiles.extend(glob(os.path.join(self.indir, sp, file_regex)))
        test_wavFiles = [os.path.split(wav)[-1] for wav in test_wavFiles]
        return train_wavFiles, test_wavFiles


    def __prepare_audio_by_group(self, wav_files, group_dir):
        """
        This method is used to prepare the "Arabic Corpus of Isolated Words"
        data for Kaldi. It should locate the preprocessed data inside
        "kaldi/egs/DATASET" where DATASET is the name of your dataset that can 
        be found in the self.dataset member variable
        """
        for filename in tqdm(wav_files, desc="Copying Train dataset"):
            speaker, rep, wordId, ext = filename.split(".")
            #create speaker directory
            safe_makedir(os.path.join(group_dir, speaker))
            filepath = os.path.join(self.indir, speaker, filename)
            newFilepath = os.path.join(group_dir, speaker, filename)
            #copy the file
            shutil.copyfile(filepath, newFilepath)


    def __create_spk2gender(self, group_dir):
        """
        This method is used to create "spk2gender" file that maps the 
        speakers to their gender following this pattern
        <speaker_id> <gender>
        According to the gender, it's either 'm' for male or
        'f' for female.
        NOTE: all speakers that we are using are male
        """
        with open(os.path.join(group_dir, "spk2gender"), "w") as fout:
            for speaker in sorted(os.listdir(group_dir)):
                if os.path.isdir(os.path.join(group_dir, speaker)):
                    fout.write("{} {}\n".format(speaker, "m"))


    def __create_wav_scp(self, group_dir):
        """
        This method is used to create "wav.scp" file that maps the
        utterance_id to the audio wav file. It should follow this pattern:
        <utterance_id> <audio abosulte path>
        utterance_id is a name that is unique for each single audio file in the data.
        So, I decided it to be following this pattern '<speakerId>_<wavName>'.
        You can use any other pattern that you find comfortable!
        """
        with open(os.path.join(group_dir, "wav.scp"), "w") as fout:
            for speaker in sorted(os.listdir(group_dir)):
                if re.match(r"S\d+", speaker):
                    if os.path.isdir(os.path.join(group_dir, speaker)):
                        wav_files = os.listdir(os.path.join(group_dir, speaker))
                        for wav_file in sorted(wav_files):
                            absPath = os.path.join(group_dir, speaker, wav_file)
                            fout.write(
                                "{}_{} {}\n".format(speaker, wav_file[:-4], absPath)
                                )


    def __create_text(self, group_dir):
        """
        This method is used to create "text" file that maps the
        utterance_id to the text. It follows this pattern:
        <utterance id> <text>
        """
        with open(os.path.join(group_dir, "text"), "w") as fout:
            for speaker in sorted(os.listdir(group_dir)):
                if re.match(r"S\d+", speaker):
                    wav_files = os.listdir(os.path.join(group_dir, speaker))
                    for wav_file in sorted(wav_files):
                        speaker, rep, wordId, ext = wav_file.split(".")
                        fout.write("{}_{} {}\n"\
                            .format(speaker, wav_file[:-4],
                                    self.WORDS[int(wordId)-1]))


    def __create_utt2spk(self, group_dir):
        """
        This method is used to create "utt2spk" file that maps the 
        utterances ids to their speaker following this pattern:
        <utterance_id> <speaker>
        """
        with open(os.path.join(group_dir, "utt2spk"), "w") as fout:
            for speaker in sorted(os.listdir(group_dir)):
                if os.path.isdir(os.path.join(group_dir, speaker)):
                    wav_files = os.listdir(os.path.join(group_dir, speaker))
                    for wav_file in sorted(wav_files):
                        fout.write("{}_{} {}\n"\
                            .format(speaker, wav_file[:-4], speaker))


    def __create_corpus(self, local_dir):
        """
        This method is used to create the text file exists in the local
        directory. This file should contain all the unique sentences
        used in the audio files.
        This file should contain every sentence in a separate line.
        """
        with open(os.path.join(local_dir, "corpus.txt"), "w") as fout:
            for word in self.WORDS:
                fout.write("{}\n".format(word))


    def __create_lexicon(self, local_dir, dict_dir):
        """
        This method is used to create the lexicon file. The lexicon
        file should map between the corpus (all text in the data) and
        the phonemes used in our system.
        NOTE: Here, I'm using my phenomizer. This phenomizer takes a
        text file as input and creates another text file containing
        the phenomes of the input based on my phoneset.
        Then, I process this file to extract only the text phoneme.
        """
        corpus_path = os.path.join(local_dir, "corpus.txt")
        phenomizer = "/media/anwar/E/PRESENTATION/Phonemizer-1.0.jar"
        subprocess.check_output(['java', '-jar', phenomizer, corpus_path])
        with open(os.path.join(local_dir, "corpus.txt")) as fin1,\
          open(os.path.join(local_dir, "corpus.txt.ph")) as fin2:
            text_lines = fin1.readlines()
            phoneme_lines = fin2.readlines()
            assert len(text_lines) == len(phoneme_lines), \
                "There is an error in the phenomizer!!"
        dict_dir = os.path.join(local_dir, "dict")  
        safe_makedir(dict_dir)
        with open(os.path.join(dict_dir, "lexicon.txt"), "w") as fout:
            #add SIL and <UNK>
            fout.write("!SIL sil\n")
            fout.write("<UNK> spn\n")
            for txt, ph in zip(text_lines, phoneme_lines):
                txt = txt.strip()
                ph = " ".join(splitPhone(ph))
                fout.write("{} {}\n".format(txt, ph))
        os.remove(os.path.join(local_dir, "corpus.txt.ph"))


    def __create_non_silence_phones(self, dict_dir):
        """
        This method is used to create non_silence phones. In other
        words, these are the phones that we pronounce that is used
        by the phonemizer.
        This method should write these non_silence_phones into a text
        file called 'non_silence_phones.txt'
        """
        phones = ['$', '@', 'A', 'P', 'R', 'S', 'T', 'a', 'a2',
                  'b', 'd', 'f', 'h', 'i', 'i2', 'l', 'm', 'n',
                  'r', 's', 't', 'w', 'x', 'y', '¥', '€']
        with open(os.path.join(dict_dir, "nonsilence_phones.txt"), "w") as fout:
            for ph in phones:
                fout.write("{}\n".format(ph))


    def __create_silence_phones(self, dict_dir, silence_phones):
        """
        This method is used to create silence phones.
        These phones are the phones that indicated that the speaker is 
        pausing and not speaking.
        This method should write these non_silence_phones into a text
        file called 'non_silence_phones.txt'
        """
        assert len(silence_phones) > 0,\
            "You have to provide silence_phones"
        with open(os.path.join(dict_dir, "silence_phones.txt"), "w") as fout:
            for ph in silence_phones:
                fout.write("{}\n".format(ph))


    def __create_optional_silence(self, dict_dir, optional_phones):
        """
        This method is used to create optional silence phones.
        These phones are the phones that indicated that the speaker is 
        pausing and not speaking.
        This method should write these non_silence_phones into a text
        file called 'non_silence_phones.txt'
        """
        assert len(optional_phones) > 0,\
            "optional_silence.txt can't be empty"
        with open(os.path.join(dict_dir, "optional_silence.txt"), "w") as fout:
            for ph in optional_phones:
                fout.write("{}\n".format(ph))


    def __copy_files(self):
        """
        This method is used to copy certain files from the 'archive' directory to
        our processed data directory at kaldi/egs.
        NOTE:Instead of copying the whole files, we will create symbolik links
        of these files. symbolic link is like a shortcut.
        """
        archive_path = os.path.abspath("archive")
        #copy archive/utils
        safe_create_symlink(src=os.path.join(archive_path, "utils"),
                            dst=os.path.join(self.OUTDIR, "utils"))
        #copy archive/steps
        safe_create_symlink(src=os.path.join(archive_path, "steps"),
                            dst=os.path.join(self.OUTDIR, "steps"))
        #copy archive/conf
        safe_create_symlink(src=os.path.join(archive_path, "conf"),
                            dst=os.path.join(self.OUTDIR, "conf"))
        #copy score.sh
        shutil.copy(src=os.path.join(archive_path, "score.sh"),
                    dst=os.path.join(self.OUTDIR, "data", "local", "score.sh"))
        #copy prepare.sh
        shutil.copy(src=os.path.join(archive_path, "prepare.sh"),
                    dst=os.path.join(self.OUTDIR, "prepare.sh"))
        #copy cmd.sh
        shutil.copy(src=os.path.join(archive_path, "cmd.sh"),
                    dst=os.path.join(self.OUTDIR, "cmd.sh"))
        #copy run_*.sh
        copy_regex(src=os.path.join(archive_path, "run_*.sh"),
                   dst=os.path.join(self.OUTDIR, "run_*.sh"))
        #create path.sh
        create_path_sh(self.OUTDIR)


    def prepare_data(self):
        # ----- Create Necessary Directories -----
        #create data directory
        safe_makedir(os.path.join(self.OUTDIR, "data"))
        #create train directory
        safe_makedir(self.TRAIN_DIR)
        test_dir = os.path.join(self.OUTDIR, "data", "test")
        safe_makedir(self.TRAIN_DIR)
        
        # ----- Prepare Audio Data -----
        train_wavfiles, test_wavfiles = self.__getAudioFiles()
        self.__prepare_audio_by_group(train_wavfiles, self.TRAIN_DIR)
        self.__prepare_audio_by_group(test_wavfiles, self.TEST_DIR)

        # ----- Prepare Mapping Files -----
        #create 'spk2gender'
        self.__create_spk2gender(self.TRAIN_DIR)
        self.__create_spk2gender(self.TEST_DIR)
        #create 'wav.scp'
        self.__create_wav_scp(self.TRAIN_DIR)
        self.__create_wav_scp(self.TEST_DIR)
        #create 'text'
        self.__create_text(self.TRAIN_DIR)
        self.__create_text(self.TEST_DIR)
        #create 'utt2spk'
        self.__create_utt2spk(self.TRAIN_DIR)
        self.__create_utt2spk(self.TEST_DIR)

        # ----- Prepare Local corpuss -----
        local_dir = os.path.join(self.OUTDIR, "data", "local")
        safe_makedir(local_dir)
        #create corpus
        self.__create_corpus(local_dir)

        # ----- Prepare Language Model -----
        dict_dir = os.path.join(local_dir, "dict")
        safe_makedir(dict_dir)
        #create lexicon
        self.__create_lexicon(local_dir, dict_dir)
        #create phones used by the phonemizer
        self.__create_non_silence_phones(dict_dir)
        #create silence phones
        self.__create_silence_phones(dict_dir, silence_phones=["sil", "spn"])
        self.__create_optional_silence(dict_dir, optional_phones=["sil"])

        # ----- Copy Data -----
        self.__copy_files()




if __name__ == "__main__":
    obj = DataOrganizer()
    obj.prepare_data()
