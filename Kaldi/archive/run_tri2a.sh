#!/bin/bash
. ./path.sh || exit 1
. ./cmd.sh || exit 1
nj=1      # number of parallel jobs - 1 is perfect for such a small dataset
lm_order=1 # language model order (n-gram quantity) - 1 is enough for our grammar
# Safety mechanism (possible running this script with modified arguments)
. utils/parse_options.sh || exit 1
[[ $# -ge 1 ]] && { echo "Wrong arguments!"; exit 1; }


echo "===== HMM TRIPHONE 2A TRAINING ====="
echo
steps/train_deltas.sh --cmd "$train_cmd" 2000 11000 data/train data/lang exp/tri1_ali exp/tri2a || exit 1
echo
echo "===== HMM TRIPHONE 2A DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri2a exp/tri2a/graph || exit 1
steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" exp/tri2a/graph data/test exp/tri2a/decode
echo
echo "===== HMM TRIPHONE 2A ALIGNMENT ====="
echo
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/train data/lang exp/tri2a exp/tri2a_ali || exit 1
echo
echo "===== run_tri2a.sh script is finished ====="
echo
