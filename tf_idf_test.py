

import pandas as pd

#TODO intergrate regex to replace urls (@^(http\:\/\/|https\:\/\/)?([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*$@i)
import re

import nltk

from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("sherpa_output.csv")

descriptions = list(df["Description"])


descriptions = [x.lower() for x in descriptions]
descriptions = [x.replace("!", " ") for x in descriptions]
descriptions = [x.replace(".", " ") for x in descriptions]
descriptions = [x.replace(",", " ") for x in descriptions]
descriptions = [x.replace("\n", " ") for x in descriptions]
descriptions = [x.replace("?", " ") for x in descriptions]
descriptions = [x.replace("'", " ") for x in descriptions]
descriptions = [x.replace(":", " ") for x in descriptions]
descriptions = [x.replace("/", " ") for x in descriptions]
descriptions = [x.replace("(", " ") for x in descriptions]
descriptions = [x.replace(")", " ") for x in descriptions]
descriptions = [x.replace("·", " ") for x in descriptions]
descriptions = [x.replace("“", " ") for x in descriptions]
descriptions = [x.replace("”", " ") for x in descriptions]



description = ''.join([i for i in descriptions if not i.isdigit()])

descriptions = [x.replace("  ", " ") for x in descriptions]


print(descriptions)

tokenized_descriptions = [nltk.word_tokenize(x) for x in descriptions]

bow = []
for doc in tokenized_descriptions:
    for word in doc:
        if word not in bow:
            bow.append(word)
            print(word)

print(bow)  # corpus bow

# print(descriptions)

doc = (descriptions[0])

def get_tf_dict(doc):
    word_dict = {}
    for word in nltk.word_tokenize(doc):
        if word not in word_dict:
            word_dict[word] = 1
        if word_dict[word] >= 1:
            word_dict[word] += 1
    return word_dict



def compute_tf(word_dict, bow):
    tf_dict = {}
    bow_len = len(bow)
    for word, count in word_dict.items():
        tf_dict[word] = count / float(bow_len)
    return tf_dict

# print(get_tf_dict(descriptions[3]))


tf_dict_list = []
for x in descriptions:
    word_dict = get_tf_dict(x)
    tf_dict = compute_tf(word_dict, bow)
    # print(tf_dict)
    tf_dict_list.append(tf_dict)

print(tf_dict_list)

# print (tf_matrix)




#
#
# vectorizer = TfidfVectorizer()
# response = vectorizer.fit_transform(descriptions)
#
# print(response)