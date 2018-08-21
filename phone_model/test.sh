#!/usr/bin/env bash

fstcompile --isymbols=test_data/phones.syms --osymbols=test_data/phones.syms test_data/k.config > test_data/k.fst

fstcompose test_data/k.fst test_data/phones.fst \
    | fstrmepsilon \
    | fstdeterminize \
    | fstminimize \
    | fstprint --isymbols=test_data/phones.syms --osymbols=test_data/phones.syms
