# Arabic Speech Recognition Using Kaldi
Kaldi is a toolkit for speech recognition written in C++ and licensed it is intended for use by speech recognition researchers. Kaldi aims to provide software that is flexible and extensible. It supports linear transforms, MMI, boosted MMI and MCE discriminative training, feature-space discriminative training, and deep neural networks.
Kaldi has been incorporated as part of the CHiME Speech Separation and Recognition Challenge over several successive events. The software was initially developed as part of a 2009 workshop at Johns Hopkins University. According to legend, Kaldi (Khaled) was the Ethiopian goat herder who discovered the coffee plant.

<p align="center">
<img src="https://www.coffeecrossroads.com/wp-content/uploads/kaldi-adapted-from-uker.png"  height="400" width="600"/> 
</p>


## Download

Before taking about installing Kaldi and the per-requisites, let’s first see how we can download it. We can do that by cloning the official repo using:
```
git clone  https://github.com/kaldi-asr/kaldi.git
```
This repo is about 200MB, so it would take some time. After downloading, a new folder named “kaldi” is created. There are a few files and sub-directories which are:

- `egs` – example scripts allowing you to quickly build ASR systems for over 30 popular speech corpora (documentation is attached for each project).
- `misc` – additional tools and supplies, not needed for proper Kaldi functionality.
- `src` – Kaldi source code.
 - `tools` – useful components and external tools.
 - `windows` – tools for running Kaldi using Windows.

The most important one are `tools/`, `src/`, and `egs/`.

## Prerequisites
Kaldi is pretty stable, but there are some prerequisites that need to be installed:

- Rule number 1 - use Linux. Although it is possible to use Kaldi on Windows, most people I find trustworthy convinced me that Linux will do the job with the less amount of problems.
 - You can install all the prerequisites in one command and that’s by running the “tools/extras/check_dependencies.sh” shell file by:
 	* Getting into “tools/” directory first using `cd kaldi/tools`.
	* Then running `extras/check_dependencies.sh` to check the dependencies.

After installing all dependencies, running this command should return:
```
$ anwar@anwar-laptop:/media/anwar/E/ASR/Kaldi/kaldi/tools$ extras/check_dependencies.sh 
extras/check_dependencies.sh: all OK.
```
The following modules are the ones that this shell script will install:

- `atlas` – automation and optimization of calculations in the field of linear algebra,
- `autoconf` – automatic software compilation on different operating systems,
- `automake` – creating portable Makefile files
- `libtool` – creating static and dynamic libraries
- `svn` – revision control system (Subversion), necessary for Kaldi download and installation
- `wget` – data transfer using HTTP, HTTPS and FTP protocols
- `zlib` – data compression.

And probably these have to be installed:

- `awk` – programming language, used for searching and processing patterns in files and data streams,
- `bash` – Unix shell and script programming language,
- `grep` – command-line utility for searching plain-text datasets for lines matching a regular expression,
 - `make` – automatically builds executable programs and libraries from source code,
- `perl` – dynamic programming language, perfect for text files processing.

## Install
The best source for installing Kaldi can be found [here](http://jrmeyer.github.io/asr/2016/01/26/Installing-Kaldi.html), but this is a simplified summarization:

- get into “tools” directory inside that folder using cd kaldi/tools.
- Check the number of cores in your processor by running nproc. The number returned from that should be used in the following command. In my case, the number was `4`.
- Now run `extras/install_irstlm.sh` to run a language modeling toolkit.
- Go to the src directory beside tools by running `cd ../src`.
- Then run `./configure`
- Then `make depend -j 4`.
- Finally, run `make -j 4`.

## Data Preparation
I have created a file that is responsible for preparing the files that Kaldi needs to train the model. The file responsible for that is called `data_preparation.py`. For more understanding about the code and what are the functionality inside it, you can check the official kadli documentation from [here](http://kaldi-asr.org/doc/kaldi_for_dummies.html). To run this script, all you have to do is install is `tqdm` pythn module. And all you need to chage about this script is these member variables:

- `dataset`: Which is the name of the dataset. I have set this variable to `arabic_corpus_of_isolated_words`.
- `indir`: Which is the full path of the downloaded data.
- `basedir`: Which is the full path of the `egs` directory of the installed kaldi.

After running this script, a new directory with the name of `dataset` variable will be created in the `basedir` directory with this hierarchy:
```
├── arabic_corpus_of_isolated_words
    ├── conf
    │   ├── mfcc.conf
    │   └── decode.config
    ├── data
    │	 ├── local
    │	 │    ├── dict
    │	 │       ├── lexicon.txt
    │	 │       ├── nonsilence_phones.txt
    │	 │       ├── optional_silence.txt
    │	 │       └── silence_phones.txt
    │	 │    ├── corpus.txt
    │	 │    └── score.sh
    │   ├── test
    │       ├── S03
    │       ├── S18
    │       ├── S12
    │       ├── ...
    │       ├── spk2gender
    │       ├── text
    │       ├── utt2spk
    │       └── wav.scp 
    │   └── train4
    │       ├── S01
    │       ├── S02
    │       ├── S04
    │       ├── ...
    │       ├── spk2gender
    │       ├── text
    │       ├── utt2spk
    │       └── wav.scp
    ├── steps -> ../../wsj/s5/steps
    ├── utils -> ../../wsj/s5/utils
    ├── cmd.sh
    ├── path.sh
    ├── run.sh
    └── score.sh

```
You should be apple to run this script like so:
```
$ python data_preparation
Copying Train dataset: 100%|███████████████████████████████████████████████████████| 7400/7400 [00:08<00:00, 892.87it/s]
Copying Train dataset: 100%|███████████████████████████████████████████████████████| 2000/2000 [00:02<00:00, 762.84it/s]
[Mar 20 15:09:32] INFO [main] [com.univox.io.ResourcesLoader:64] - Loaded Phonemizer Resources.
[Mar 20 15:09:32] INFO [main] [com.univox.PhonemizerMain:45] - Statement: صفر
[Mar 20 15:09:32] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _SfR_
[Mar 20 15:09:32] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ S f R _

[Mar 20 15:09:32] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:32] INFO [main] [com.univox.PhonemizerMain:45] - Statement: واحد
[Mar 20 15:09:32] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _wa2xd_
[Mar 20 15:09:32] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ w a2 x d _

[Mar 20 15:09:32] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:32] INFO [main] [com.univox.PhonemizerMain:45] - Statement: إثنان
[Mar 20 15:09:32] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _€¥na2n_
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ € ¥ n a2 n _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: ثلاثة
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _¥la2¥tt_
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Applied Rule: FIND [tt][_] REPLACE [h][_]
Output: _ ¥ l a2 ¥ h _
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ ¥ l a2 ¥ h _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: أربعة
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _€Rb@tt_
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Applied Rule: FIND [tt][_] REPLACE [h][_]
Output: _ € R b @ h _
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ € R b @ h _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: خمسة
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _Pmstt_
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Applied Rule: FIND [tt][_] REPLACE [h][_]
Output: _ P m s h _
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ P m s h _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: ستة
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _sttt_
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Applied Rule: FIND [tt][_] REPLACE [h][_]
Output: _ s t h _
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ s t h _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: سبعة
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _sb@tt_
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Applied Rule: FIND [tt][_] REPLACE [h][_]
Output: _ s b @ h _
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ s b @ h _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: ثمانية
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _¥ma2nytt_
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Applied Rule: FIND [tt][_] REPLACE [h][_]
Output: _ ¥ m a2 n y h _
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ ¥ m a2 n y h _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: تسعة
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _ts@tt_
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Applied Rule: FIND [tt][_] REPLACE [h][_]
Output: _ t s @ h _
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ t s @ h _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: التنشيط
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _a2ltn$yT_
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،التنشيط،" -- "_ a2 l t n $ y T _" failed in this rule "FIND [_][a2]".
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،التنشيط،" -- "_ a2 l t n $ y T _" failed in this rule "FIND [_][VWLS]".
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ a2 l t n $ y T _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: التحويل
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _a2ltxwyl_
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،التحويل،" -- "_ a2 l t x w y l _" failed in this rule "FIND [_][a2]".
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،التحويل،" -- "_ a2 l t x w y l _" failed in this rule "FIND [_][VWLS]".
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ a2 l t x w y l _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: الرصيد
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _a2lRSyd_
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،الرصيد،" -- "_ a2 l R S y d _" failed in this rule "FIND [_][a2]".
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،الرصيد،" -- "_ a2 l R S y d _" failed in this rule "FIND [_][VWLS]".
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ a2 l R S y d _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: التسديد
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _a2ltsdyd_
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،التسديد،" -- "_ a2 l t s d y d _" failed in this rule "FIND [_][a2]".
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،التسديد،" -- "_ a2 l t s d y d _" failed in this rule "FIND [_][VWLS]".
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ a2 l t s d y d _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: نعم
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _n@m_
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ n @ m _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: لا
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _la2_
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ l a2 _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: التمويل
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _a2ltmwyl_
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،التمويل،" -- "_ a2 l t m w y l _" failed in this rule "FIND [_][a2]".
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،التمويل،" -- "_ a2 l t m w y l _" failed in this rule "FIND [_][VWLS]".
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ a2 l t m w y l _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: البيانات
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _a2lbya2na2t_
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،البيانات،" -- "_ a2 l b y a2 n a2 t _" failed in this rule "FIND [_][a2]".
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،البيانات،" -- "_ a2 l b y a2 n a2 t _" failed in this rule "FIND [_][VWLS]".
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ a2 l b y a2 n a2 t _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: الحساب
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _a2lxsa2b_
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،الحساب،" -- "_ a2 l x s a2 b _" failed in this rule "FIND [_][a2]".
[Mar 20 15:09:33] ERROR [main] [com.univox.phonemizer.ValidationRule:31] - Line number "1": "،الحساب،" -- "_ a2 l x s a2 b _" failed in this rule "FIND [_][VWLS]".
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ a2 l x s a2 b _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:45] - Statement: إنهاء
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:77] - Transcribe: _€nha2€_
[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:89] - Final Output: _ € n h a2 € _

[Mar 20 15:09:33] INFO [main] [com.univox.PhonemizerMain:90] - *****************************************************************************
```
**Very Imporant**:
Starting from the thrid line in the previous output; you won't get these lines as these are related to the phenomizer that I used. A phenomizer is a software that converts text word to a sequence of phoemes like `صفر` to `S F R`. I can't share the one that I used with you as it doesn't belong to me. You need to create yours.

## Train Model
Now, we have prepared our data for training. You can do that simply by running `run.sh` shell script in the root directory of the data. Mine is `/media/anwar/E/ASR/Kaldi/kaldi/egs/arabic_corpus_of_isolated_words` which is the same as `indir` member variable.

If you have made any mistakes in this tutorial, logs from the terminal should guide you how to deal with it. [Here is](http://www.mediafire.com/file/m43428auuz1i2k8/run_log.txt/file) my terminal output that you should get something similar to it, you can download it for reference.


## Getting Results
The decoding results in the terminal window, go to newly made `kaldi/egs/DATASET/exp` where `DATASET` is the name of the dataset (mine is `arabic_cropus_of_isolated_words`. You may notice there folders with `mono` and `tri1` results as well. Here you may find result files named in a `wer_{number}` way.

The test Word Error Rate of your trained model can be found inside `exp/X/decode/wer_{number}` where `X` is the trained model name. For example, the `wer_17` of the HMM mono model can be found at `exp/mono/deocde/wer_17` which would look like this:
```
compute-wer --text --mode=present ark:exp/mono/decode/scoring/test_filt.txt ark,p:- 
%WER 0.80 [ 16 / 2000, 3 ins, 0 del, 13 sub ]
%SER 0.80 [ 16 / 2000 ]
Scored 2000 sentences, 0 not present in hyp.
```
As we can see, our HMM mono model got a wer (word error rate) of `0.80%` with getting only 16 wrong. if you want to do more analysis and see which words our model got it wrong, you can check `exp/mono/decode/log/decode.1.log` file which would look like this:
```
S03_S03.01.01 صفر 
LOG (gmm-latgen-faster[5.5.249~1-461b5]:DecodeUtteranceLatticeFaster():decoder-wrappers.cc:289) Log-like per frame for utterance S03_S03.01.01 is -8.33501 over 94 frames.
S03_S03.01.02 واحد 
LOG (gmm-latgen-faster[5.5.249~1-461b5]:DecodeUtteranceLatticeFaster():decoder-wrappers.cc:289) Log-like per frame for utterance S03_S03.01.02 is -8.19328 over 98 frames.
S03_S03.01.03 إثنان 
LOG (gmm-latgen-faster[5.5.249~1-461b5]:DecodeUtteranceLatticeFaster():decoder-wrappers.cc:289) Log-like per frame for utterance S03_S03.01.03 is -8.0858 over 88 frames.
S03_S03.01.04 ثلاثة 
LOG (gmm-latgen-faster[5.5.249~1-461b5]:DecodeUtteranceLatticeFaster():decoder-wrappers.cc:289) Log-like per frame for utterance S03_S03.01.04 is -7.73602 over 120 frames.
...
```
As you can see, the file name is on the right, and the predicted text is on the left.

### Visualizing Lattice
If you want to do more analysis, thanks to [Josh Meyer's blog](http://jrmeyer.github.io/asr/2016/12/15/Visualize-lattice-kaldi.html), you can visualize the lattice object that kaldi produced using our test data. You can do that by using `utils/show_lattice.sh` file. You can use it like so:
```
$ utils/show_lattice.sh [--mode display|save] [--format pdf|svg] <utt-id> <lattice-ark> <word-list>
```
But first, we need to intall `graphviz` library using `sudo apt-get install graphviz`

After installing you can visualize the lattice object of a certain test file. Let's say that we want to visualize the lattice object of `S03_S03.01.01`, then we can go to the root directory of our data which is `kaldi/egs/arabic_corpus_of_isolated_words` and run:
```
$ ./utils/show_lattice.sh S03_S03.01.01 ./exp/mono/decode/lat.1.gz ./exp/mono/graph/words.txt
```
This command consists of four parts:

- `./utils/show_lattice.sh`: which is the shell script that generates the visualization.
- `S03_S03.01.01`: which is the utterance id of the test file`S03.01.01.wav`.
- `./exp/mono.deocde/lat.1.gz`: which is the lattic-ark object.
- `./exp/mono/graph/words.txt`: which is the filet that contain words and their ids.
The output of this command should be a pdf file named `S03_03.01.01.pdf` at the current directory containing lattice visualization that looks like this:

<p align="center">
<img src="http://www.mediafire.com/convkey/c33b/rqp3f93esks1b3azg.jpg"  height="200" width="400"/> 
</p>

You can open the `utils/decode` file and change the `lm_scale` and `acoustic_scale` parameters. Here, I used the zero values.

TO BE CONTINUEUED :)