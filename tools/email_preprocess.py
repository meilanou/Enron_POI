#!/usr/bin/python

import pickle
import cPickle
import numpy as np
import math

from sklearn import cross_validation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif


def preprocess(keys_file, features_file, labels_file, text_type=None, \
               max_doc_freq=0.5, min_doc_freq=1, select_percentile=10):
    """ 
        this function takes a pre-made list of email texts (by default word_data.pkl)
        and the corresponding authors (by default email_authors.pkl) and performs
        a number of preprocessing steps:
            -- splits into training/testing sets (10% testing)
            -- vectorizes into tfidf matrix
            -- selects/keeps most helpful features

        after this, the feaures and labels are put into numpy arrays, which play nice with sklearn functions

        4 objects are returned:
            -- training/testing features
            -- training/testing labels

    """

    # load data
    emails_file_handler = open(keys_file, "r")
    emails = pickle.load(emails_file_handler)
    emails_file_handler.close()

    features_file_handler = open(features_file, "r")
    features = pickle.load(features_file_handler)
    features_file_handler.close()

    labels_file_handler = open(labels_file, "r")
    labels = cPickle.load(labels_file_handler)
    labels_file_handler.close()

    ### text vectorization--go from strings to lists of numbers
    if text_type == "email": # treat the entire email address as one word
        # tried ^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$ and \S+, didn't work as desired
        # there are email headers that have 2 dots e.g. a..howard@enron.com
        # also email headers have no dot e.g. 40enron@enron.com
        vectorizer = CountVectorizer(token_pattern="(\w+(?:\.+\w+)*@\w+(?:\.\w+)+)", \
                                     max_df=max_doc_freq, min_df=min_doc_freq)
    elif text_type == "dict":
        vectorizer = DictVectorizer()
    else:
        vectorizer = TfidfVectorizer(sublinear_tf=True, stop_words="english", \
                                     max_df=max_doc_freq, min_df=min_doc_freq)
        
    features_vectorized = vectorizer.fit_transform(features)

    ### feature selection, because text is super high dimensional and 
    ### can be really computationally chewy as a result
    selector = SelectPercentile(f_classif, percentile=select_percentile)
    selector.fit(features_vectorized, labels)
    features_vectorized_selected = selector.transform(features_vectorized)

    feature_names = vectorizer.get_feature_names()

    no_selected = features_vectorized_selected.shape[1]
    indices_selected = [i for i in np.argsort(selector.scores_)[::-1]][:no_selected]
    indices_selected.sort() # features will be returned by index order not score ranking

    # buid reference list for selected feature names
    feature_names = vectorizer.get_feature_names()
    feature_names_selected = [feature_names[i] for i in indices_selected]
    # buid reference list for selected scores
    scores_selected = [selector.scores_[i] for i in indices_selected]
    # (feature index, feature name, feature core)
    names_scores = zip(indices_selected, feature_names_selected, scores_selected)

    ### display info of the data
    print 'no. of data points =', len(labels)
    print 'no. of features vectorized =', features_vectorized.shape[1]
    print 'no. of features selected =', no_selected

    
    return emails, features_vectorized_selected.toarray(), labels, names_scores
