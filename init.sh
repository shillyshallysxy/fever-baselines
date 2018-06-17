#!/bin/bash

mkdir -p data/fever-data

maybe_download()
{
    # arg1: target path, arg2: url
    if ! [ -e $1 ]; then
        echo "wget -O $1 $2"
        wget -O $1 $2
    else
        echo "file $1 exists. skipping wget..."
    fi
}
#To replicate the paper, download paper_dev and paper_test files. These are concatenated for the shared task
maybe_download data/fever-data/train.jsonl https://s3-eu-west-1.amazonaws.com/fever.public/train.json
maybe_download data/fever-data/dev.jsonl https://s3-eu-west-1.amazonaws.com/fever.public/paper_dev.jsonl
maybe_download data/fever-data/test.jsonl https://s3-eu-west-1.amazonaws.com/fever.public/paper_test.jsonl

if ! [ -d data/glove ]; then
wget http://nlp.stanford.edu/data/wordvecs/glove.6B.zip
unzip glove.6B.zip -d data/glove
gzip data/glove/*.txt
fi

if ! [ -d data/wiki-pages ]; then
wget https://s3-eu-west-1.amazonaws.com/fever.public/wiki-pages.zip
unzip wiki-pages.zip -d data
fi

# construct database
if ! [ -e data/fever/fever.db ]; then
    PYTHONPATH=src python3 src/scripts/build_db.py data/wiki-pages data/fever/fever.db
fi

# sampling
PYTHONPATH=src python3 src/scripts/dataset/neg_sample_evidence.py data/fever/fever.db

