#!/usr/bin/python

import pickle
import numpy
numpy.random.seed(42)
import sys
sys.path.append("tools/")
from sklearn import tree
from sklearn.metrics import accuracy_score
from email_preprocess import preprocess

### the words/emails (features) and POI classifications (labels), already largely processed
### these files should have been created from the previous (Lesson 10) mini-project.
features_path = "corpus_features_bcc.pkl" 
labels_path = "corpus_labels.pkl"

# get Tfidf training and testing sets
features_train, features_test, labels_train, labels_test, vectorizer = \
                preprocess(features_path, labels_path, test_size=0.2, entire_string=True,\
                           max_doc_freq=1.0, min_doc_freq=1, select_percentile=100)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features_train, labels_train)
pred = clf.predict(features_test)
accuracy = accuracy_score(pred, labels_test)

print 'accuracy =', accuracy

# 1st time (almost) all words
# 2nd time "sshacklensf" removed from text_learning/vectorize_text.py
# 3rd time "cgermannsf" removed

feature_importances = zip(clf.feature_importances_, vectorizer.get_feature_names())

import pprint
pp = pprint.PrettyPrinter(indent=4)

print 'top 5 importances & feature names'
pp.pprint(sorted(feature_importances,key=lambda x: x[0], reverse=True)[:5])


