#!/usr/bin/env bash

# Example usage
#       ./run.sh kaideng dakai_diandeng

# compile fst
fstcompile --isymbols=test_data/phones.syms --osymbols=test_data/grammar.syms \
    test_data/kai_deng.config > test_data/kai_deng.fst

# find shortest path
fstcompose test_data/kai_deng.fst test_data/grammar.fst \
    | fstshortestpath \
    | fsttopsort \
    | fstrmepsilon \
    | fstprint --isymbols=test_data/phones.syms --osymbols=test_data/grammar.syms

# output should be something like this
#
#   0       1       k       开      0.694147706
#   1       2       k       <epsilon>
#   2       3       k       <epsilon>
#   3       4       <blank> <epsilon>
#   4       5       <blank> <epsilon>
#   5       6       ai1     <epsilon>
#   6       7       <blank> <epsilon>
#   7       8       <blank> <epsilon>
#   8       9       d       灯      1.9647696
#   9       10      <blank> <epsilon>
#   10      11      <blank> <epsilon>
#   11      12      eng1    <epsilon>
#   12      0.367724776