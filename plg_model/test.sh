#!/usr/bin/env bash

fstcompile --isymbols=test_data/phones.syms --osymbols=test_data/phones.syms \
    test_data/kai_deng.config > test_data/kai_deng.fst

fstcompose test_data/kai_deng.fst test_data/plg.fst \
    | fstshortestpath \
    | fsttopsort \
    | fstrmepsilon \
    | fstprint --isymbols=test_data/phones.syms --osymbols=test_data/grammar.syms