#!/bin/bash
. ./path.sh || exit 1
. ./cmd.sh || exit 1
nj=1      # number of parallel jobs - 1 is perfect for such a small dataset
lm_order=1 # language model order (n-gram quantity) - 1 is enough for our grammar
# Safety mechanism (possible running this script with modified arguments)
. utils/parse_options.sh || exit 1
[[ $# -ge 1 ]] && { echo "Wrong arguments!"; exit 1; }


echo "===== HMM TRIPHONE 3C TRAINING ====="
echo
steps/train_mpe.sh data/train data/lang exp/tri2b_ali exp/tri2b_denlats exp/tri3c || exit 1
echo
echo "===== HMM TRIPHONE 3C DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri3c exp/tri3c/graph || exit 1
steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" exp/tri3c/graph data/test exp/tri3c/decode
echo
echo "===== run_tri3c.sh script is finished ====="
echo
