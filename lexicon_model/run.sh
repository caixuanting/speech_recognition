#!/usr/bin/env bash

# Usage:
#       lexicon_model/run.sh lexicon_model example/lexicon_model dict.txt phones.syms example/grammar_model grammar.syms

python $1/dict_to_fst.py $2 $3

fstcompile --isymbols=$2/$4 --osymbols=$5/$6 $2/lexicon.init > $2/lexicon.fst

# create lexicon.fst
for file in `ls $2/*.config`
do
    fstcompile --isymbols=$2/$4 --osymbols=$5/$6 ${file} > ${file}.fst
    fstunion ${file}.fst $2/lexicon.fst | fstarcsort --sort_type=ilabel > $2/temp.fst
    mv $2/temp.fst $2/lexicon.fst
done

# clean up
rm $2/*.config
rm $2/*.config.fst

# print
# example/lexicon_model/lexicon.fst \
#   | fstprint --isymbols=example/lexicon_model/phones.syms --osymbols=example/grammar_model/texts.syms
