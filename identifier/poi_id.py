#!/usr/bin/python

import sys
import pickle
sys.path.append("tools/")
import math
import numpy as np

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
# You will need to use more features

##features_list = ['poi','total_payments','salary','bonus','deferred_income',\
##                 'exercised_stock_options','restricted_stock','total_stock_value', \
##                 'from_messages', 'to_messages', \
##                 'from_poi_to_this_person', 'from_this_person_to_poi', \
##                 'shared_receipt_with_poi']

features_list = ['poi', 'bonus', 'exercised_stock_options', 'corpus_score']

print 'features_list', features_list

### Load the dictionary containing the dataset
# final_project_dataset.pkl has 146 keys
# final_project_dataset_modified.pkl has 143 keys
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )
data_dict_corpus = pickle.load(open("corpus_link_to_scores_dict.pkl", "r") )



### Task 2: Remove outliers

### First, remove total and agency
data_dict.pop('TOTAL', 0)
#data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)

### Task 3: Create new feature(s)

poi_no = 0
non_no = 0

for (k, v) in data_dict.items():
    # log transform monetary value
    # 1 dollar to represent NONE
    try:
        v["bonus"] = math.log(float(v["bonus"])) if v["bonus"] != "NaN" else 0
    except ValueError:
        v["bonus"] = -2
    try:
        v["exercised_stock_options"] = math.log(float(v["exercised_stock_options"])) if v["exercised_stock_options"] != "NaN" else 0
    except ValueError:
        v["exercised_stock_options"] = -2
    # find corpus_score for current row
    scores = [(a, b) for a, b in data_dict_corpus.items() if a == v["email_address"]]
    if len(scores) < 1:
        if v["poi"] == True: poi_no += 1
        else: non_no += 1
        data_dict[k]["corpus_score"] = 0.
    else:
        data_dict[k]["corpus_score"] = scores[0][1]["corpus_score"]


# scale feature values to mean = 0 stdev = 1
import pandas as pd
from sklearn import preprocessing

data_df = pd.DataFrame(data_dict).transpose()
feat_only_list = list(features_list)
feat_only_list.remove("poi")
poi_df = data_df[["poi"]].copy()
feat_df = data_df[feat_only_list].copy()
scaled_df = pd.DataFrame(preprocessing.scale(feat_df), columns=feat_only_list)
scaled_df.index = poi_df.index
data_df = pd.concat([poi_df, scaled_df], axis=1)
data_df = data_df.transpose()
data_dict = data_df.to_dict()

### Store to my_dataset for easy export below.
my_dataset = data_dict



### Extract features and labels from dataset for local testing
# default parameters:
# remove_NaN = True, remove_all_zeroes = True, remove_any_zeroes = False, sort_keys = False
data = featureFormat(my_dataset, features_list)
labels, features = targetFeatureSplit(data)
print 'no. of extracted data points by features', len(labels)


### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# note that major classifier testing code is in classifiers_testing.pyc

from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(3)


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script.
### Because of the small size of the dataset, the script uses stratified
### shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# run grid search to find better parameter combination

from sklearn import grid_search

parameters = {"n_neighbors": [2, 5],
              "weights": ["uniform", "distance"],
              "p":[1, 2]}
clf = KNeighborsClassifier()
gscv = grid_search.GridSearchCV(clf, parameters, scoring="f1_micro")
gscv.fit(features, labels)
print gscv.best_params_

# NO scoring func
# {'n_neighbors': 2, 'weights': 'uniform', 'p': 1}
# scoring="average_precision"
# {'n_neighbors': 2, 'weights': 'distance', 'p': 1}
# scoring="recall"
# {'n_neighbors': 2, 'weights': 'distance', 'p': 2}


clf = KNeighborsClassifier(n_neighbors=2, weights="distance", p=1)
test_classifier(clf, my_dataset, features_list)


### Dump your classifier, dataset, and features_list so 
### anyone can run/check your results.

dump_classifier_and_data(clf, my_dataset, features_list)




