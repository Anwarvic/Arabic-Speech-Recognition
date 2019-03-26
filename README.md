# Arabic Speech Recognition
In this repoitory, I'm going to create an Automatic Speech Recognition model for Arabic language using a couple of the most famous Automatic Speech Recognition free-ware framework:

- [Kaldi](http://kaldi-asr.org/): The most famous ASR framework.
- [CMU-Sphinx](http://www.speech.cs.cmu.edu/sphinx/doc/Sphinx.html): The famous framework by Carnegie Mellon University.

In this repository, you can see just two folders "Kaldi" and "Sphinx". The `Kaldi` directory contains my Arabic ASR model using kaldi, and the `Sphinx` directory contains my Arabic ASR model using cmu-sphinx4. Inside each directory, you can find `README.md` that explains how to download, install and use the framework.

## Download Dataset

This dataset is a small open-source dataset called the "Arabic Corpus of Isolated Words" made by the [University of Stirling](http://www.cs.stir.ac.uk/) located in the Central Belt of Scotland. This dataset can be downloaded from the official website right [here](http://www.cs.stir.ac.uk/~lss/arabic/). The "Arabic speech corpus for isolated words" contains about 10,000 utterances (9992 utterances to be precise) of 20 words spoken by 50 native male Arabic speakers. It has been recorded with a 44100 Hz sampling rate and 16-bit resolution in the raw format (.wav files). This corpus is free for noncommercial uses.

After downloading the dataset and extracting it, you will find about 50 folders with the name of "S+speakerId" like so S01, S02, ... S50. Each one of these folders contains around 200 audio files, each audio file contains the audio of the speaker speaking just one word. Notice that the naming of these audio files has certain information that we surely need. So for example the audio file named as "S01.02.03.wav", this means that the wav was created by the speaker whose id is "1", saying the word "03" which is "اثنان", for the "second" repetition. Each speaker has around 200 wav files, saying 20 different words 10 times. And these words are:
```
d = {
        "01": "صِفْرْ", 
        "02":"وَاحِدْ",
        "03":"إِثنَانِْ",
        "04":"ثَلَاثَةْ",
        "05":"أَربَعَةْ",
        "06":"خَمْسَةْ",
        "07":"سِتَّةْ",
        "08":"سَبْعَةْ",
        "09":"ثَمَانِيَةْ",
        "10":"تِسْعَةْ",
        "11":"التَّنْشِيطْ",
        "12":"التَّحْوِيلْ",
        "13":"الرَّصِيدْ",
        "14":"التَّسْدِيدْ",
        "15":"نَعَمْ",
        "16":"لَا",
        "17":"التَّمْوِيلْ",
        "18":"الْبَيَانَاتْ",
        "19":"الْحِسَابْ",
        "20":"إِنْهَاءْ"
        }
```