#!/usr/bin/env bash

# compile fst for kai
fstcompile --isymbols=test_data/phones.syms --osymbols=test_data/phones.syms \
    test_data/kai_deng.config > test_data/kai_deng.fst

# check kai is valid
fstcompose test_data/kai_deng.fst test_data/lexicon.fst \
    | fstrmepsilon \
    | fstprint --isymbols=test_data/phones.syms --osymbols=test_data/grammar.syms


# output should be something like this
#
#   0       1       k       开
#   1       2       ai1     <epsilon>
#   2
