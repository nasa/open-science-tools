
import pandas as pd

pubs =  pd.read_csv('nasa_publications_division_spending.csv')


filtered = pubs[pubs['Division']!='SciAct']
filtered = filtered[filtered['Division']!='OSTEM']
filtered = filtered[filtered['Division']!='OSSI']


data_train = filtered.sample(frac=0.8, random_state=389)
data_test = filtered.loc[~filtered.index.isin(data_train.index)]

data_train.to_csv("nasa_publication_train_set.csv", columns=['Article Title','Journal Name', 'Division'])
data_test.to_csv("nasa_publication_test_set.csv" , columns=['Article Title','Journal Name', 'Division'])
