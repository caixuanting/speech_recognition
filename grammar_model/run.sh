#!/usr/bin/env bash

# Example usage
#       grammar_model/run.sh example/grammar_model/texts

# generate word symbols
# words are separated by space
ngramsymbols < $1.txt > $1.syms

# convert words to symbols
farcompilestrings --symbols=$1.syms --keep_symbols=1 $1.txt > $1.far

# output counts of n-grams
ngramcount $1.far > $1.cnts

# make n-gram model
ngrammake $1.cnts > $1.mod

# rename model file
mv $1.mod $1.fst

# clean up
rm $1.cnts
rm $1.far

