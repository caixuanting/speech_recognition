#!/usr/bin/env bash

fstcompile --isymbols=test_data/phones.syms --osymbols=test_data/phones.syms test_data/kai_deng.config > test_data/kai_deng.fst

fstcompose test_data/kai_deng.fst test_data/phones.fst \
    | fstshortestpath \
    | fsttopsort \
    | fstrmepsilon \
    | fstprint --isymbols=test_data/phones.syms --osymbols=test_data/phones.syms

# output
#   0       1       k       k
#   1       2       k       <epsilon>
#   2       3       k       <epsilon>
#   3       4       <blank> <blank>
#   4       5       <blank> <blank>
#   5       6       ai1     ai1
#   6       7       <blank> <blank>
#   7       8       <blank> <blank>
#   8       9       d       d
#   9       10      <blank> <blank>
#   10      11      <blank> <blank>
#   11      12      eng1    eng1
#   12