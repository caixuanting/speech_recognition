#!/usr/bin/env bash

# Example usage:
#       phone_model/run.sh phone_model example/phone_model phones.syms

# create fst config file for phones
python $1/phone_to_fst.py $2 phones.txt

# create initial phones.fst
fstcompile --isymbols=$2/$3 --osymbols=$2/$3 $2/phones.init > $2/phones.fst

# create combined phones.fst
for file in `ls $2/*.config`
do
    fstcompile --isymbols=$2/$3 --osymbols=$2/$3 ${file} > ${file}.fst
    fstunion ${file}.fst $2/phones.fst | fstclosure > $2/temp.fst
    mv $2/temp.fst $2/phones.fst
done

# clean up
rm $2/*.config
rm $2/*.config.fst

# copy result to test_data
cp $2/phones.fst phone_model/test_data/phones.fst

# print result
# fstrmepsilon example/phone_model/phones.fst \
#   | fstprint --isymbols=example/phone_model/phones.syms --osymbols=example/phone_model/phones.syms