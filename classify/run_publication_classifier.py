import sys

import numpy as np
import pandas as pd


def publication_classifier(title, journal, name_dict, word_dict, div_list=['APD', 'ESD', 'HPD', 'PSD', 'BPS','STMD', 'SOMD', 'ESDMD', 'ARD', 'OTH']):
    """Given a title and a journal name, return the most likely division and a set of probabilities
    """
    # Determine the journal probability.  If the journal is not detected, set the probability to even
    try:
       p_name = name_dict[journal]
    except:
       p_name = np.ones(len(div_list)) / len(div_list)

    p_words = np.zeros(len(div_list))
    weights = 0
    for t in title.split():
        try:
             wei = abs(word_dict[t].max() - np.median(word_dict[t]))**3
             p_words = p_words + wei * word_dict[t]
             weights += wei
        except KeyError:
             pass
    p_words = p_words / p_words.sum()

    if p_name.max() == 1:
       p_total = p_name
    else:
       p_total = p_words * p_name

    return div_list[p_total.argmax()], p_total


def read_name_dict(infile = 'distribution_journal_name.tsv'):
   """Read in the journal name dictionary"""
   name_dict = {}
   with open(infile, 'r') as jin:
         jin.readline()
         for fp in jin:
             fp = fp.split('\t')
             name = fp[0]
             dist = np.array([float(x) for x in fp[1:]])
             name_dict[name] = dist

   return name_dict


def read_word_dict(infile = 'distribution_title_word.tsv'):
   """Read in the word dictionary"""
   word_dict = {}
   with open(infile, 'r') as win:
         win.readline()
         for fp in win:
             fp = fp.split('\t')
             word = fp[0]
             dist = np.array([float(x) for x in fp[1:]])
             word_dict[word] = dist

   return word_dict


if __name__ == '__main__':
   
   import os
   import argparse

   parser = argparse.ArgumentParser(
                    prog='run_publication_classifier',
                    description='Given a title and Journal name, classify the publication by NASA division')
   parser.add_argument('title', help='title of an article')
   parser.add_argument('journal', help='jounral name for the article')
   args = parser.parse_args()


   print(args.title)
   print(args.journal)


   # set up 


   # read in the name dictionary
   name_dict = read_name_dict()


   # return the probabilities of the different divisions
   word_dict = read_word_dict()

   d, p = publication_classifier(args.title, args.journal, name_dict, word_dict)
   print(d, p)
