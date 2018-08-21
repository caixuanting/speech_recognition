#!/usr/bin/env bash

# compile fst for kai
fstcompile --isymbols=test_data/phones.syms --osymbols=test_data/phones.syms \
    test_data/kai.config > test_data/kai.fst

# check kai is valid
fstcompose test_data/kai.fst test_data/lexicon.fst \
    | fstrmepsilon \
    | fstdeterminize \
    | fstminimize \
    | fstprint --isymbols=test_data/phones.syms --osymbols=test_data/texts.syms


# output should be something like this
#
#   0       1       k       开
#   1       2       ai1     <epsilon>
#   2
