# -*- coding:utf-8 -*-
import pymysql
import traceback
import datetime
import requests
import json
import re
import jieba as jb
from gensim import corpora, models, similarities
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# seg_list = jb.cut("我来到了美丽的复旦大学，太漂亮了啊。可是我还是喜欢上海外滩。正如我们知道的那样，上海自来水来自海上, shit.",cut_all=False)
# print("/".join(seg_list))


def jieba_cut(text):
    return " ".join(jb.cut(text, cut_all=False))

documents = [jieba_cut("白日依山尽，黄河入海流"),jieba_cut("床前明月光，疑是地上霜"),jieba_cut("举头望明月，低头思故乡"),jieba_cut("黑夜给了我黑色的眼睛，我却用它寻找光明。")]
print("documents:")
print(documents)

texts = [[word for word in document.split()] for document in documents]
# texts = [[document] for document in documents]
print("texts:")
print(texts)

dictionary = corpora.Dictionary(texts)
dictionary.save('temorary_dict.dic')
# dictionary = corpora.Dictionary.load('temporary_dict.dic')
# print(dictionary)
print("dictionary:")
print(dictionary)
print("tokens-id:")
print(dictionary.token2id)

corpus = [dictionary.doc2bow(text) for text in texts]
print("corpus:")
print(corpus)
corpora.MmCorpus.serialize('corpus.mm', corpus)
# corpus = corpora.MmCorpus('corpus.mm')
# print(len(corpus))


new_documents = [jieba_cut("白日依山尽，黄河入海流"),jieba_cut("黑夜给了我黑色的眼睛，我却用它寻找光明。")]
# good_documents = [jieba_cut("白日依山尽，黄河入海流")]

tfidf = models.TfidfModel(corpus=corpus)
tfidf.save('model.tfidf')

vector = tfidf[new_documents]
corpora.MmCorpus.serialize('tfidf.mm', tfidf_corpus)

print('vector:')
for doc in vector:
    print(doc)


# corpus_tfidf = tfidf[corpus]


print(tfidf.dfs)
print(tfidf.idfs)

lsi = models.LsiModel(corpus=vector, id2word=dictionary, num_topics=2)
lsi.print_topics(2)
corpus_lsi = lsi[vector]
for doc in corpus_lsi:
    print(doc)

index = similarities.MatrixSimilarity(lsi[corpus])

query = jieba_cut("在地上，我自在地依山，灼人的白日，对的。")
print(query)
# query_bow = dictionary.doc2bow(query)
query_bow = dictionary.doc2bow(query.split())
print(query_bow)
query_lsi = lsi[query_bow]
print(query_lsi)
sims = index[query_lsi]
print(list(enumerate(sims)))
sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sort_sims)


