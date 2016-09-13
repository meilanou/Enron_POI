#!/usr/bin/python

import pickle
import sys
sys.path.append("tools/")
import math
import numpy as np
from sklearn import decomposition, preprocessing

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier

# turn actions on or off
use_new_feature, scale_features = True, True
plot_vis, test_PCA = False, False
check_boundaries, check_k_folds = False, True
folds, step_size = 1000, .1

# Select what features to use.

##features_list = ['poi',\
##                 'salary', 'bonus', 'long_term_incentive', 'deferred_income', \
##                 'deferral_payments', 'loan_advances', 'other', 'expenses', \
##                 'director_fees', 'total_payments', 'exercised_stock_options', 'restricted_stock', \
##                 'email_address', 'restricted_stock_deferred', 'total_stock_value', \
##                 'to_messages', 'from_messages', 'from_this_person_to_poi', 'from_poi_to_this_person', \
##                 'shared_receipt_with_poi']

##features_list = ['poi',\
##                 'salary', 'bonus', 'long_term_incentive', 'deferred_income', \
##                 'deferral_payments', 'loan_advances', 'other', 'expenses', \
##                 'director_fees', 'total_payments', 'exercised_stock_options', 'restricted_stock', \
##                 'restricted_stock_deferred', 'total_stock_value']

##features_list = ['poi', 'deferred_income', 'exercised_stock_options', 'total_payments','restricted_stock_deferred']

#features_list = ['poi', 'bonus', 'exercised_stock_options', 'deferred_income']
features_list = ['poi', 'exercised_stock_options', 'corpus_score', 'bonus'] #, 'corpus_score'

##features_list = ['poi','total_payments','bonus','deferred_income',\
##                 'total_stock_value','exercised_stock_options','restricted_stock']

##features_list = ['poi','total_payments','total_stock_value','deferred_income']



### Load the dictionary containing the dataset
# final_project_dataset.pkl has 146 keys
# final_project_dataset_modified.pkl has 143 keys
#data_dict = pickle.load(open("final_project_dataset.pkl", "r"))
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )
data_dict_corpus = pickle.load(open("corpus_link_to_scores_dict.pkl", "r") )

# Remove outliers
data_dict.pop('TOTAL', None)

# Create new feature(s)
if use_new_feature == True:
    for (k, v) in data_dict.items():
        # 1 dollar to represent NONE
        try:
            v["bonus"] = math.log(float(v["bonus"])) if v["bonus"] != "NaN" else 0
        except ValueError:
            v["bonus"] = -2
        try:
            v["exercised_stock_options"] = math.log(float(v["exercised_stock_options"])) if v["exercised_stock_options"] != "NaN" else 0
        except ValueError:
            v["exercised_stock_options"] = -2 
        scores = [(a, b) for a, b in data_dict_corpus.items() if a == v["email_address"]]
        if len(scores) < 1:
            data_dict[k]["corpus_score"] = 0.
        else:
            data_dict[k]["corpus_score"] = scores[0][1]["corpus_score"]
            
    #features_list.remove("salary")
    #features_list += ["total_payments_log", "total_stock_log", "deferred_income_log"]
            
if scale_features == True:
    import pandas as pd
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


print 'features_list len', len(features_list)
print features_list

### Extract features and labels from dataset for local testing
# default parameters:
# remove_NaN = True, remove_all_zeroes = True, remove_any_zeroes = False, sort_keys = False
data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)
print 'no. extracts by features', len(labels)

# plot to see data distribution
if plot_vis == True:
    from data_vis import draw_data
    draw_data(features_list, features, labels)

# PCA finding
if test_PCA == True:
    # scale data with mean = 0 and stdev = 1
    features_scaled = preprocessing.scale(features)
    
    pca = decomposition.PCA(n_components=2)#n_components=4
    transformed = pca.fit_transform(features_scaled)
    #print pca.components_
    print pca.explained_variance_ratio_

    # plot to see PCA weights
    from data_vis import draw_PCA
    draw_PCA(transformed, pca.components_.T, features_list[1:], \
             arrow_size=5.0, text_pos=5.5)

# test with a variety of classifiers
if check_k_folds == True:
    from classifiers_testing import run_k_folds
    run_k_folds(data_dict, features_list, folds=folds)
    
if check_boundaries == True:
    from classifiers_testing import plot_boundaries
    plot_boundaries(data_dict, features_list, step_size=step_size, test_size=0.1)

    





