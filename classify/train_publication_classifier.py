import sys

import numpy as np
import pandas as pd


data_train =  pd.read_csv('nasa_publication_train_set.csv')



print(pd.unique(data_train['Division']))

div_dict = {'APD':0, 'ESD':1, 'HPD':2, 'PSD':3, 'BPS':4,'STMD':5, 'SOMD':6, 'ESDMD':7, 'ARD':8, 'OTH':9}
div_list = list(div_dict.keys())
n_division = len(div_dict)


# Determine the unique journal names and for each one 
names = pd.unique(data_train['Journal Name'])
name_dict = {}

for n in names:
    name_dict[n] = np.zeros(n_division)
    d = data_train[data_train['Journal Name'] == n]['Division']
    count = 0.0
    for i in d.map(lambda x: div_dict[x.strip()]):
        name_dict[n][i] += 1
        count += 1
    name_dict[n] = name_dict[n] / count

fout = open('distribution_journal_name.tsv', 'w')
str_out = "Journal Name\t" + '\t'.join(div_dict.keys())+'\n'
fout.write(str_out)
for k in name_dict.keys(): 
    str_out = k + '\t' + '\t'.join([str(x) for x in name_dict[k]])+'\n'
    fout.write(str_out)
fout.close()

# Determine the frequency of different words corresponding to divisions
word_dict = {}

title_list = data_train['Article Title'].to_list()
division_list = data_train['Division'].to_list()

for title,division in zip(title_list, division_list):
    title = ''.join([i.lower() for i in title if i.isalpha() or i==' ']) #prep the title
    index = div_dict[division.strip()]
    for w in title.split():
        try:
            word_dict[w][index] +=1 
        except KeyError:
            word_dict[w] = np.zeros(n_division)
            word_dict[w][index] +=1

for w in word_dict.keys():
    word_dict[w] = word_dict[w] / word_dict[w].sum()

fout = open('distribution_title_word.tsv', 'w')
str_out = "Title Word\t" + '\t'.join(div_dict.keys())+'\n'
fout.write(str_out)
for k in word_dict.keys(): 
    str_out = k + '\t' + '\t'.join([str(x) for x in word_dict[k]])+'\n'
    fout.write(str_out)
exit()

def model(title, journal, name_dict, word_dict, div_list):
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



# Step through the test data set and determine how well the model can predict the data
title_test = data_test['Article Title'].to_list()
journal_test = data_test['Journal Name'].to_list()
division_test = data_test['Division'].to_list()


count = 0
correct = 0

for title, journal, division in zip(title_test, journal_test, division_test):
    title = ''.join([i.lower() for i in title if i.isalpha() or i==' '])
    d, p = model(title, journal, name_dict, word_dict, div_list)
    title = ''.join([i.lower() for i in title if i.isalpha() or i==' '])
    d, p = model(title, journal, name_dict, word_dict, div_list)
    count += 1
    if d == division:
       correct += 1

    #else:
       #print(title, journal, division, d, p)
#
#
       ##if journal in name_dict.keys():
          #print("   ", journal, name_dict[journal])
       #else:
           #print("   ", journal)
       #p_word = np.zeros(len(div_list))
       #for t in title.split():
           #if t in word_dict.keys():
              #print("   ", t, word_dict[t])
              #p_word = p_word + word_dict[t]
           #else:
              #print("   ", t)
       #print("   ", p_word/p_word.sum())
print(count, correct, correct / count)


pubs['Guess Division'] = ''
titles = pubs['Article Title'].tolist()
journals = pubs['Journal Name'].tolist()

for i in range(len(titles)):
    title = titles[i]
    journal = journals[i]
    title = ''.join([i.lower() for i in title if i.isalpha() or i==' '])
    d, p = model(title, journal, name_dict, word_dict, div_list)
    pubs.loc[i, 'Guess Division'] = d

pubs.to_csv('guess.csv')

exit()






