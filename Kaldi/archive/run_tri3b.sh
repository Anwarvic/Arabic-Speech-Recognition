#!/bin/bash
. ./path.sh || exit 1
. ./cmd.sh || exit 1
nj=1      # number of parallel jobs - 1 is perfect for such a small dataset
lm_order=1 # language model order (n-gram quantity) - 1 is enough for our grammar
# Safety mechanism (possible running this script with modified arguments)
. utils/parse_options.sh || exit 1
[[ $# -ge 1 ]] && { echo "Wrong arguments!"; exit 1; }


echo "===== HMM TRIPHONE 3B TRAINING ====="
echo
steps/train_mmi.sh --boost 0.05 data/train data/lang exp/tri2b_ali exp/tri2b_denlats exp/tri3b || exit 1
echo
echo "===== HMM TRIPHONE 3B DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri3b exp/tri3b/graph || exit 1
steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" exp/tri3b/graph data/test exp/tri3b/decode
echo
echo "===== run_tri3b.sh script is finished ====="
echo
