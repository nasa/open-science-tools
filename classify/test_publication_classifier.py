

import sys

import numpy as np
import pandas as pd
from run_publication_classifier import publication_classifier, read_name_dict, read_word_dict

# read in the distributions
name_dict = read_name_dict()
word_dict = read_word_dict()


data_test =  pd.read_csv('nasa_publication_test_set.csv')


# Step through the test data set and determine how well the model can predict the data
title_test = data_test['Article Title'].to_list()
journal_test = data_test['Journal Name'].to_list()
division_test = data_test['Division'].to_list()


count = 0
correct = 0

for title, journal, division in zip(title_test, journal_test, division_test):
    title = ''.join([i.lower() for i in title if i.isalpha() or i==' '])
    d, p = publication_classifier(title, journal, name_dict, word_dict)
    count += 1
    if d == division:
       correct += 1

print(count, correct, correct / count)



