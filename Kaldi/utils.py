import os
import subprocess


def safe_makedir(dirname):
    """
    Creates a directory recursively if not existed
    """
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def splitPhone(ph):
    """
    This function is used to extract single phonemes out of a stream of
    phonemes. It takes the phoneme stream as input and returns a list of
    single phonemes.
    >>> splitPhone("")
    """
    ph = ph.strip()
    ph = ph.strip("_")
    length = len(ph)
    output = []
    for i in range(length-1):
        if ph[i].isdigit():
            continue
        elif not ph[i].isdigit() and ph[i+1].isdigit():
            output.append(ph[i] + ph[i+1])
        else:
            output.append(ph[i])
    if not ph[length-1].isdigit():
        output.append(ph[length-1])
    return output


def safe_create_symlink(src, dst):
    """
    This function creates symbolic link using the src (source) directory
    and copy it to the dst (destination) directory
    """
    if not os.path.exists(dst):
        os.symlink(src, dst)

def create_path_sh(data_dir):
    """
    This function is used to create path.sh shell file based on the
    data_dir input
    """
    content =\
"""
# Defining Kaldi root directory
export KALDI_ROOT=`pwd`/../..
# Setting paths to useful tools
export PATH=$PWD/utils/:$KALDI_ROOT/src/bin:$KALDI_ROOT/tools/openfst/bin:$KALDI_ROOT/src/fstbin/:$KALDI_ROOT/src/gmmbin/:$KALDI_ROOT/src/featbin/:$KALDI_ROOT/src/lmbin/:$KALDI_ROOT/src/sgmm2bin/:$KALDI_ROOT/src/fgmmbin/:$KALDI_ROOT/src/latbin/:$PWD:$PATH
# Defining audio data directory (modify it for your installation directory!)
export DATA_ROOT="{}"
# Enable SRILM
. $KALDI_ROOT/tools/env.sh
# Variable needed for proper data sorting
export LC_ALL=C
""".format(data_dir)
    with open(os.path.join(data_dir, "path.sh"), "w") as fout:
        fout.write(content.strip())