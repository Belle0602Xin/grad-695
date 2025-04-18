# %% [code]
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in


import os
import pdb
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json as js


import nltk
import gensim
from gensim import corpora, models
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer,SnowballStemmer
from nltk.stem.porter import *


from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

"""
There is no fixed solution for anaconda pyLDAvis installation deprecated warnings
"""
import matplotlib.pyplot as plt
import pyLDAvis
import pyLDAvis.sklearn
from wordcloud import WordCloud, STOPWORDS
import csv
import xlrd
import xlsxwriter


import random
import copy
import collections
import re
from operator import itemgetter
import seaborn as sns


from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import *
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn import mixture



import tensorflow as tf
import tensorflow_hub as hub
import bert
from tensorflow.keras.models import Model


from bert_implementation import *
from randomforests_related import *
from svm_related import *

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

# %% [code]
# clean up data
stemmer = SnowballStemmer('english')
vocab_size = 10000



"""
extract verb from text
"""
def lemmatize_stemming(text):
    return stemmer.stem(text)
    #return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


"""
clear trivial words such as a, an, the and so forth
"""
def preprocess_stem_clean(text):
    result = []
    """
    Convert a document into a list of tokens.
    This lowercases, tokenizes, de-accents (optional). – 
    the output are final tokens = unicode strings, that won’t be processed any further.
    """
    for token in simple_preprocess(text):
        if token not in STOPWORDS and token not in ['al','cd','et','en','el','da','de','lo','la','le','rt']:
            result.append(lemmatize_stemming(token))
    return result


def remove_punctuation(string):

    # punctuation marks
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    # traverse the given string and if any punctuation
    # marks occur replace it with null
    for x in string.lower():
        if x in punctuations:
            string = string.replace(x, "")

            # Print string without punctuation
    return string.split(' ')


# %% [code]
def preprocess_data():
    i,k = 0,0
    # word related to diagnositics and surveillance
    related_words = ['diagnostic', 'diagnostics', 'symptomatic', 'diagnosing', 'diagnosis', 'clinical',
                     'diagnose', 'diagnoses', 'detection', 'screening', 'analytical', 'assessment',
                    'prognosis', 'surveillance', 'monitoring', 'reconnaissance']
    spreadsheet_match = []
    corona_abstract_all_text = []
    corona_body_all_text = []

    keywords_list = []

    """
    walk through all the files under specific directory
    """
    for dirname, _, filenames in os.walk('C:/PythonWorkspace/document_parses/pdf_json'):
        for filename in filenames:
            #print(os.path.join(dirname, filename))

            topic_related = False
            # this variable is used to determine how many sections may exist
            author_cnt=0
            if i % 1000 == 0:
                print ("Working (number %d)..." % i)

            """
            This is for test purpose
            """
            # if i==200:
            #     return corona_body_all_text, corona_abstract_all_text, spreadsheet_match, keywords_list

            """
            only load json files
            """
            if filename.split(".")[-1] == "json":

                f = open(os.path.join(dirname, filename))
                j = js.load(f)
                f.close()

                """
                some articles contain abstract while others not 
                """
                try:
                    abstract_text = ' '.join([x['text'] for x in j['abstract']])
                except:
                    abstract_text = ''

                """
                extract all the keywords
                """
                tmp=''
                name = ''
                # d represents each individual dictionary
                # j['body_text'] is a python list which contains many dictionaries
                for d in j['body_text']:
                    # preprocess the data which will bu put in csv file

                    if author_cnt<1:
                        for dic in j['metadata']['authors']:
                            name += dic['first'] + ' ' + dic['last']
                            name += ', '
                        name = name[:-2]
                        author_cnt+=1


                    if d['section']=='Keywords':
                        tmp+=d['text']
                        keywords_list.append(tmp)

                spreadsheet_match.append([j['paper_id'], j['metadata']['title'], name, i, 1])

                i+=1


                """
                body text and abstract consist the whole body text
                """
                body_text = ' '.join(x['text'] for x in j['body_text'])
                body_text += ' ' + abstract_text

                """
                for related_word in related_words:
                    if related_word in body_text:
                        topic_related = True
                        break
                if topic_related:
                    if abstract_text:
                        corona_pos_all_text.append(abstract_text)
                """

                # append abstract content
                if abstract_text:
                    k+=1
                    corona_abstract_all_text.append(abstract_text)
                # append body text content
                corona_body_all_text.append(body_text)
        print(i)
        print(k)
    return corona_body_all_text, corona_abstract_all_text, spreadsheet_match, keywords_list



"""
we use wordCloud library to show the most frequent words in each cluster 
"""
def word_cloud_advanced(corona_pos_all_text):

    """
    wordCloud only accepts string as input
    """
    stopwords=set(STOPWORDS)
    res = ''
    for text in corona_pos_all_text:
        for word in text:
            res += word + ' '

    # generate wordcloud image
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(res)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('wordcloud_original')
    plt.show()


"""
this function is to generate the histogram
"""
def generate_histogram(corona_body_all_text):
    # corona_hist = [len(preprocess_stem_clean(x)) for x in corona_body_all_text]
    # remove all the punctuations at the very beginning
    corona_hist = [len(re.findall(r'\w+', x))  for x in corona_body_all_text]
    plt.hist(corona_hist,bins='auto',color='#0504aa',alpha=0.7)
    # plt.bar([i for i in range(len(corona_pos_all_text))], corona_pos_all_text)
    plt.xlabel('Number of words')
    plt.ylabel('Number of articles')
    plt.savefig('histogram.pdf')
    plt.show()



def initial_spreadsheet(spreadsheet_match):
    # match_shuffled = random.sample(spreadsheet_match, len(spreadsheet_match))[:100]

    workbook=xlsxwriter.Workbook('spreadsheet.xlsx')
    worksheet=workbook.add_worksheet('My sheet')

    header=['paper_id','title','authors','paper_number','label']
    for k in range(len(header)):
        worksheet.write(0,k,header[k])

    for i in range(1,201):
        for j in range(len(spreadsheet_match[0])):
            worksheet.write(i,j,spreadsheet_match[i-1][j])
    workbook.close()




def initial_csv(spreadsheet_match):

    # no_match_shuffled = random.sample(keywords_no_match, len(keywords_no_match))[:100]
    spreadsheet_match=spreadsheet_match[:200]

    file=open('labels.csv','w+',newline='',encoding='utf-8')
    # identifying header
    header=[['paper_id','title','authors','paper_number','label']]

    # writing data row-wise into the csv file
    with file:
        write=csv.writer(file)
        write.writerows(header)
        write.writerows(spreadsheet_match)



"""
dimension reduction
"""
def tfidf_LDA(corona_body_all_text):
    corpus=[]
    for text in corona_body_all_text:
        corpus.append(' '.join(text))

    # the features of each data are 900 now
    vectorizer=TfidfVectorizer(max_features=1500, stop_words='english')
    corpus_matrix=vectorizer.fit_transform(corpus)
    print(corpus_matrix.shape)


    # the most representative top 1500 words in corona_body_all_text
    # the basic structure is like a python dictionary
    word_feature_list=vectorizer.get_feature_names()
    corpus_matrix=corpus_matrix.toarray()
    return corpus_matrix,word_feature_list


"""
return the labels and number of specific paper
"""
def generate_labels():
    y=[]
    indices=[]
    loc = ('labels.xlsx')

    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    # return labels and number of the paper
    for i in range(1,sheet.nrows):
        y.append(int(sheet.cell_value(i, 4)))
        indices.append(int(sheet.cell_value(i,3)))
    return y,indices


"""
grid search function
"""
def grid_search(corpus_matrix,y,indices,spreadsheet_match):
    # this is for unbalanced problems
    cw=collections.Counter(y)

    # examples of grid search
    parameters = [{'kernel': ['rbf'], 'gamma': [1, 0.1, 1e-2, 1e-3, 1e-4], 'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000], 'class_weight':[cw]},
                  {'kernel': ['linear'], 'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000], 'class_weight':[cw]}]

    grid = GridSearchCV(SVC(), parameters, refit=True, verbose=3, scoring='f1')

    X = []
    for i in range(len(corpus_matrix)):
        if i in indices:
            # train on 200 papers
            X.append(corpus_matrix[i])

    X=np.array(X)
    y=np.array(y)
    corpus_matrix=np.array(corpus_matrix)


    clf = grid.fit(X, y)

    # print(clf.best_params_)
    # print(clf.best_estimator_)
    # print()

    # predict on the entire dataset
    y_score_rbf = clf.decision_function(corpus_matrix)

    # this yields the minimum and maximum value of svm regressor output
    print(str(min(y_score_rbf)) + '   ' + str(max(y_score_rbf)))
    print()

    """
    this is the test of all dataset 
    """
    y_pred=clf.predict(corpus_matrix)
    workbook=xlsxwriter.Workbook('spreadsheet_SVM_prediction.xlsx')
    worksheet=workbook.add_worksheet('My sheet')

    # rewrite features and labels to a file, this is different from the initial file
    # write the header first
    header=['paper_id','title','authors','paper_number','label']
    for k in range(len(header)):
        worksheet.write(0,k,header[k])

    for i in range(1, len(corpus_matrix) + 1):
        for j in range(len(spreadsheet_match[0])):
            worksheet.write(i, j, spreadsheet_match[i-1][j])
            worksheet.write(i, 4, y_pred[i-1])
    workbook.close()
    """
    this is the test of entire dataset
    """


    def normalization(data):
        _range = np.max(data) - np.min(data)
        return (data - np.min(data)) / _range

    # this is for f1_score, recall, accuracy and ROC curve
    training_score = clf.decision_function(X)
    training_score_normalization = normalization(training_score)
    training_label = clf.predict(X)
    print('accuracy ' + str(accuracy_score(y, training_label)))
    print('f1_score ' + str(f1_score(y, training_label)))
    print('precision_score '+str(precision_score(y,training_label)))
    print('recall_score ' + str(recall_score(y, training_label)))

    fpr, tpr, threshold = roc_curve(y, training_score_normalization)

    # plot the ROC curve
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2)
    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('The ROC curve')
    plt.savefig('ROC_curve.pdf')
    plt.show()

    # return index of a sorted list
    sorted_indices = sorted(range(len(y_score_rbf)), key=lambda k: y_score_rbf[k])

    # get the paper numbers which are not in the training set
    subtract_indices = []
    for val in sorted_indices:
        if val not in indices:
            subtract_indices.append(val)

    # get top 10%, bottom 10% and middle 10%
    res = []
    res += subtract_indices[:67]
    res += subtract_indices[-67:]
    res += subtract_indices[len(sorted_indices) // 2:len(sorted_indices) // 2 + 33]
    res += subtract_indices[len(sorted_indices) // 2 - 33:len(sorted_indices) // 2]

    workbook = xlsxwriter.Workbook('spreadsheet_svm.xlsx')
    worksheet = workbook.add_worksheet('My sheet')

    # write to a file without labels, this is different from the initial file
    # each paper is labeled 1 automatically at the very beginning
    # then we need to label each paper manually
    header = ['paper_id', 'title', 'authors', 'paper_number', 'label']
    for k in range(len(header)):
        worksheet.write(0, k, header[k])

    for i in range(1, len(res) + 1):
        for j in range(len(spreadsheet_match[0])):
            worksheet.write(i, j, spreadsheet_match[res[i - 1]][j])
    workbook.close()


"""
Only keep the words with the top-5000 tfidf words.
"""
def process_word(text, word_feature_list):
    result = []
    for p in text:
        temp = []
        for w in p:
            if w in word_feature_list:
                temp.append(w)
        if len(temp) != 0:
            result.append(temp)
    result=np.array(result)
    return result



"""
data preprocessing and wordcloud operation
"""
corona_body_all_text, corona_abstract_all_text, spreadsheet_match, keywords_list = preprocess_data()
print('The total number of documents is '+str(len(corona_body_all_text)))
print('The total number of items in spreadsheet is '+str(len(spreadsheet_match)))
print('The total number of documents which contain keywords is '+str(len(keywords_list)))


keywords_all_text = [preprocess_stem_clean(x) for x in keywords_list]
word_cloud_advanced(keywords_all_text)


"""
get histogram visualization
"""
# generate_histogram(corona_body_all_text)


"""
this body_all_text below is after stem cleaning
"""
body_all_text = [preprocess_stem_clean(x) for x in corona_body_all_text]
"""
this body_all_text is for entire words
"""
# tmp_list=corona_body_all_text.copy()
# body_all_text = [remove_punctuation(x) for x in tmp_list]


"""
dimension reduction
"""
corpus_matrix,word_feature_list=tfidf_LDA(body_all_text)
print('dimensional reduction is done')
print()


"""
initial spreadsheet visualization
"""
# initial_csv(spreadsheet_match)
# initial_spreadsheet(spreadsheet_match)


"""
SVM iterations to generate the pre-trained model
this also includes hyperparameter tuning models 
"""
y,indices=generate_labels()
# generate_SVM(corpus_matrix,y,indices,spreadsheet_match)
grid_search(corpus_matrix,y,indices,spreadsheet_match)
# k_fold_svm(corpus_matrix,y,indices,spreadsheet_match)

print('This is the end')



"""
randomforests to test the pre-trained model
"""
# randomforests_predict(corpus_matrix,y,indices,spreadsheet_match)
# test_randomforests(corpus_matrix)



"""
BERT  Algorithm Implementation
"""
# embeddings_info=generate_bert(corona_abstract_all_text)
# print(len(embeddings_info))
# print(len(embeddings_info[0]))
