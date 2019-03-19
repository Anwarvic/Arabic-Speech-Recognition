# Arabic Speech Recognition Using Kaldi
Kaldi is a toolkit for speech recognition written in C++ and licensed it is intended for use by speech recognition researchers. According to legend, Kaldi (Khaled) was the Ethiopian goat herder who discovered the coffee plant.

<p align="center">
<img src="https://www.coffeecrossroads.com/wp-content/uploads/kaldi-adapted-from-uker.png" /> 
</p>


## Download

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


### 1. “tools/” sub-directory

The directory "tools/' is where we install things that Kaldi depends on in various ways. Look very quickly at the file`INSTALL` which gives instructions on how to install the tools. The most important sub-directory of “tools/” is “openfst/”. OpenFst is a library for constructing, combining, optimizing, and searching weighted finite-state transducers (FSTs). If you ever want to understand Kaldi deeply you will need to understand OpenFst. For this, the best starting point is here.

### 2. “src/” sub-directory

The directory "src/' is where all the code and executables (binary files which is ended by “.bin”) are located. Inside this directory, you will see a few files and a large number of sub-directories. You can test the existing code/files by running make test. This command goes into the various sub-directories and runs test programs in there. All the tests should succeed. 

### 3.“egs/” sub-directory

The directory "egs/' is where example scripts are located allowing us to quickly build ASR systems for over 30 popular speech corpora (documentation is attached for each project).

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
The main source for installing Kaldi can be found [here](http://jrmeyer.github.io/asr/2016/01/26/Installing-Kaldi.html), but these are a simplified summarization:

- get into “tools” directory inside that folder using cd kaldi/tools.
- Check the number of cores in your processor by running nproc. The number returned from that should be used in the following command. In my case, the number was `4`.
- Now run `extras/install_irstlm.sh` to run a language modeling toolkit.
- Go to the src directory beside tools by running `cd ../src`.
- Then run `./configure`
- Then `make depend -j 4`.
- Finally, run `make -j 4`.
