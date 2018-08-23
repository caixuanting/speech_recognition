#!/usr/bin/env bash

# Example usage:
#       plg_model/run.sh example/phone_model/phones.fst example/lexicon_model/lexicon.fst example/grammar_model/grammar.fst example/plg_model/plg.fst
fstcompose $1 $2 |  fstcompose - $3 | fstclosure > $4

#fstprint --isymbols=$5 --osymbols=$6 $4/plg.fst