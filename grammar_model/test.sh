#!/usr/bin/env bash

# Example usage
#       ./run.sh kaideng dakai_diandeng

# compile fst
fstcompile --isymbols=test_data/texts.syms --osymbols=test_data/texts.syms \
    test_data/kaideng.txt > test_data/kaideng.fst

fstcompile --isymbols=test_data/texts.syms --osymbols=test_data/texts.syms \
    test_data/dakai_diandeng.txt > test_data/dakai_diandeng.fst

fstunion test_data/kaideng.fst test_data/dakai_diandeng.fst | fstclosure > test_data/test_commands.fst

# find shortest path
fstcompose test_data/test_commands.fst test_data/texts.fst \
    | fstshortestpath \
    | fstrmepsilon \
    | fsttopsort \
    | fstprint --isymbols=test_data/texts.syms --osymbols=test_data/texts.syms

# clean up
rm test_data/*.fst

# output should be something like this
#
#   0       1       打开    打开    1.69414771
#   1       2       电灯    电灯    2.9647696
#   2       0.367724776