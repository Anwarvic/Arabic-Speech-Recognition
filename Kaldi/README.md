# Arabic Speech Recognition Using Kaldi
Kaldi is a toolkit for speech recognition written in C++ and licensed it is intended for use by speech recognition researchers. According to legend, Kaldi (Khaled) was the Ethiopian goat herder who discovered the coffee plant.

<p align="center">
<img src="https://www.coffeecrossroads.com/wp-content/uploads/kaldi-adapted-from-uker.png" /> 
</p>


##Download
Before taking about installing Kaldi and the per-requisites, let’s first see how we can download it. We can do that by cloning the official repo using:
```
git clone  https://github.com/kaldi-asr/kaldi.git
```
This repo is about 200MB, so it would take some time. After downloading, a new folder named “kaldi” is created. There are a few files and sub-directories which are:

- `egs` – example scripts allowing you to quickly build ASR systems for over 30 popular speech corpora (documentation is attached for each project),
  - `misc` – additional tools and supplies, not needed for proper Kaldi functionality,
- `src` – Kaldi source code.
 - `tools` – useful components and external tools.
 - `windows` – tools for running Kaldi using Windows.

The most important one are `tools/`, `src/`, and `egs/` that will be discussed in more details.


###1. “tools/” sub-directory
The directory "tools/' is where we install things that Kaldi depends on in various ways. Look very quickly at the file`INSTALL` which gives instructions on how to install the tools. The most important sub-directory of “tools/” is “openfst/”. OpenFst is a library for constructing, combining, optimizing, and searching weighted finite-state transducers (FSTs). If you ever want to understand Kaldi deeply you will need to understand OpenFst. For this, the best starting point is here.

###2. “src/” sub-directory
The directory "src/' is where all the code and executables (binary files which is ended by “.bin”) are located. Inside this directory, you will see a few files and a large number of sub-directories. You can test the existing code/files by running make test. This command goes into the various sub-directories and runs test programs in there. All the tests should succeed. 

### 3.“egs/” sub-directory
The directory "egs/' is where example scripts are located allowing us to quickly build ASR systems for over 30 popular speech corpora (documentation is attached for each project).
