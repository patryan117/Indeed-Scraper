

import pandas as pd
#TODO add dict comprehension to filter out size of top_bow_dict (add size as a parameter)
#TODO pad each string with spaces so that java wont throw True for javascript and java.  "java" -> " java ".
import re
import nltk
import numpy
import math




from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("sherpa_output.csv")
descriptions_list = list(df["Description"])


descriptions_list = [x.lower() for x in descriptions_list]
descriptions_list = [x.replace("!", " ") for x in descriptions_list]
descriptions_list = [x.replace(".", " ") for x in descriptions_list]
descriptions_list = [x.replace(",", " ") for x in descriptions_list]
descriptions_list = [x.replace("\n", " ") for x in descriptions_list]
descriptions_list = [x.replace("?", " ") for x in descriptions_list]
descriptions_list = [x.replace("'", " ") for x in descriptions_list]
descriptions_list = [x.replace(":", " ") for x in descriptions_list]
descriptions_list = [x.replace("/", " ") for x in descriptions_list]
descriptions_list = [x.replace("(", " ") for x in descriptions_list]
descriptions_list = [x.replace(")", " ") for x in descriptions_list]
descriptions_list = [x.replace("·", " ") for x in descriptions_list]
descriptions_list = [x.replace("“", " ") for x in descriptions_list]
descriptions_list = [x.replace("”", " ") for x in descriptions_list]
descriptions_list = [x.replace("|", " ") for x in descriptions_list]
descriptions_list = [x.replace("  ", " ") for x in descriptions_list]

regex = re.compile('^a-zA-Z')
descriptions_list = [regex.sub("", x) for x in descriptions_list]                   # [["this is america'],["something something something"], ...]
tokenized_descriptions_list = [nltk.word_tokenize(x) for x in descriptions_list]    # [["this","is","america'],["something", "something", "something"], ...]



global char_limit
char_limit = 2

global top_bow_limit
top_bow_limit = 20000



# makes top bow (dict), inputting a dict that holds the terms by their frequency in the global dictionary

def get_top_bow_dict(tok_doc_list):
    global_word_dict = {}
    for doc in tok_doc_list:
        for word in doc:
            if len(word) >= char_limit:
                if word not in global_word_dict:
                    global_word_dict[word] = 1
                if global_word_dict[word] >= 1:
                    global_word_dict[word] += 1

    ordered_top_dict= {}
    for x in range(len(global_word_dict)):
        word = max(global_word_dict, key = global_word_dict.get)
        ordered_top_dict[x] = word
        del global_word_dict[word]

    return(ordered_top_dict)

top_bow_dict = get_top_bow_dict(tokenized_descriptions_list)
print(top_bow_dict)




def get_tf_dict_list(tok_doc_list, top_bow_dict):
    tf_idf_dict_list = []
    for doc in tok_doc_list:
        tf_dict_per_doc = {}
        total_word_count = len(doc)

        for num in range(len(top_bow_dict)):
            word = top_bow_dict[num]
            counter = doc.count(word)
            tf_dict_per_doc[num] = (counter / total_word_count)
        tf_idf_dict_list.append(tf_dict_per_doc)
    return tf_idf_dict_list


tf_dict_list = get_tf_dict_list(tokenized_descriptions_list, top_bow_dict)
# print(tf_dict_list)



for x in tf_dict_list:
    print(x)




print()


# # ln (total number of documents, number of occourences of i word)

def get_idf_dict(tok_docs_list, top_bow_dict):

    num_docs = len(tok_docs_list)
    idf_dict = {}
    for num in range(len(top_bow_dict)):
        counter = 0
        for doc in tok_docs_list:
            counter += doc.count(top_bow_dict[num])
        idf_dict[num] = math.log10(num_docs / float(counter))
    return idf_dict

idf_dict = get_idf_dict(tokenized_descriptions_list, top_bow_dict)
print(idf_dict)




# convert tf_dict to list:
idf_list = []
for x in range(len(idf_dict)):
    idf_list.append(idf_dict[x])

print(idf_list)



















#
#
# def get_bow(doc_list):
#
#     bow = []
#     for doc in tokenized_descriptions_list:
#         for word in doc:
#             if len(word) >= char_limit:
#                 if word not in bow:
#                     bow.append(word)
#     return bow
#
# bow = get_bow(descriptions_list)
#
#
#
# def get_tf_dict(doc):
#     word_dict = {}
#     for word in nltk.word_tokenize(doc):
#         if len(word) >= char_limit:
#             if word not in word_dict:
#                 word_dict[word] = 1
#             if word_dict[word] >= 1:
#                 word_dict[word] += 1
#     return word_dict
#
#
#
# def compute_tf(word_dict, bow):
#     tf_dict = {}
#     bow_len = len(bow)
#     for word, count in word_dict.items():
#         tf_dict[word] = count / float(bow_len)
#     return tf_dict
#
#
#
# tf_dict_list = []
# for x in descriptions_list:
#     word_dict = get_tf_dict(x)
#     tf_dict = compute_tf(word_dict, bow)
#     tf_dict_list.append(tf_dict)
#
#
#
# # ln (total number of documents, number of occourences of i word)
# def  compute_idf_dict(doc_list, bow):
#     num_docs = len(doc_list)
#     idf_dict = {}
#     for word in bow:
#         word_freq = 0
#         for x in range(len(doc_list)):
#             if word in doc_list[x]:
#                 word_freq += 1
#         try:
#             idf_dict[word] = math.log10( num_docs / float(word_freq))
#         except:
#             idf_dict[word] = 0
#     return(idf_dict)
#
#
#
#
# idf_vec = compute_idf_dict(descriptions_list, bow)
#
#
#
# print(tf_dict)
#












# def compute_idf(doc_list):
#
#     idf_dict = {}
#     n = len(doc_list)
#
#     idf_dict = dict.fromkeys(doc_list[0].keys(), 0)
#     print(idf_dict)
#     for doc in doc_list:
#         for word, val in doc.items():
#             if val > 0:
#                     idf_dict += 1
#     for word, val in idf_dict.items():
#         idf_dict[word] = math.log10( n / float(val))
#
#     return idf_dict

# idf_list = compute_idf(descriptions)




