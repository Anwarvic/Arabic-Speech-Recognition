#!/bin/bash
. ./path.sh || exit 1
. ./cmd.sh || exit 1
nj=1      # number of parallel jobs - 1 is perfect for such a small dataset
lm_order=1 # language model order (n-gram quantity) - 1 is enough for our grammar
# Safety mechanism (possible running this script with modified arguments)
. utils/parse_options.sh || exit 1
[[ $# -ge 1 ]] && { echo "Wrong arguments!"; exit 1; }


echo "***** HMM Triphone Using SAT *****"
echo "===== HMM TRIPHONE 3D TRAINING ====="
echo
steps/train_sat.sh --cmd "$train_cmd" 2000 11000 data/train data/lang exp/tri2b_ali exp/tri3d || exit 1
echo
echo "===== HMM TRIPHONE 3D DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri3d exp/tri3d/graph || exit 1
steps/decode_fmllr.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" exp/tri3d/graph data/test exp/tri3d/decode
echo
echo "===== HMM TRIPHONE 3D ALIGNMENT ====="
echo
steps/align_fmllr.sh --nj $nj --cmd "$train_cmd" data/train data/lang exp/tri3d exp/tri3d_ali || exit 1
echo
echo "===== HMM TRIPHONE 3D DENOMINATOR LATTICES ====="
echo
steps/make_denlats.sh --nj $nj --cmd "$train_cmd" data/train data/lang exp/tri3d exp/tri3d_denlats || exit 1;
echo
echo "===== run_tri3d.sh script is finished ====="
echo
