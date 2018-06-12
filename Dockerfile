FROM continuumio/miniconda3

ENTRYPOINT ["/bin/bash", "-c"]

RUN mkdir /fever/
VOLUME /fever/
ADD requirements.txt /fever/
ADD setup.py /fever/
ADD src /fever/
ADD config /fever/

RUN apt-get update
RUN conda update -q conda
RUN conda info -a
RUN conda create -q -n fever python=3.6
RUN apt-get update && apt-get install -y build-essential gcc
RUN . activate fever
WORKDIR /fever
RUN pip install --upgrade protobuf 
RUN pip install --no-cache-dir -r requirements.txt
RUN python setup.py install

# indexing
RUN PYTHONPATH=/fever python scripts/build_db.py data/wiki-pages data/fever/fever.db
RUN PYTHONPATH=/fever python scripts/build_tfidf.py data/fever/fever.db data/index/

# sampling
# Using random sampling method
RUN PYTHONPATH=/fever python scripts/dataset/neg_sample_evidence.py data/fever/fever.db
