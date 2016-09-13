#!/usr/bin/python

import pickle
import sys
sys.path.append("tools/")
import math
import numpy as np

from feature_format import featureFormat, targetFeatureSplit


### Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

features_list = ['poi','total_payments','salary','bonus','deferred_income',\
                 'exercised_stock_options','restricted_stock','total_stock_value', \
                 'from_messages', 'to_messages', \
                 'from_poi_to_this_person', 'from_this_person_to_poi', \
                 'shared_receipt_with_poi']

##features_list = ['poi','total_payments','total_stock_value']

# final_project_dataset.pkl has 146 keys
# final_project_dataset_modified.pkl has 143 keys
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )

print "no. total available features =", len(data_dict[data_dict.keys()[0]])

### Remove outliers, if needed
data_dict.pop('TOTAL', 0)


for f in features_list:
    print "{} values missing for {}".format(sum([1 for x,y in data_dict.items() if y[f] == "NaN"]), f)

sys.exit()
##for k, v in data_dict.items():
##    t = float(v['total_payments'])
##    t = 0 if math.isnan(t) else t
##    x = float(v['deferral_payments'])
##    x = 0 if math.isnan(x) else x
##    y = float(v['deferral_payments'])
##    y = 0 if math.isnan(y) else y
##    v['test'] = (x+y)/t if t > 0 else 0

### Extract features and labels from dataset for local testing
# default parameters:
# remove_NaN = True, remove_all_zeroes = True, remove_any_zeroes = False
data = featureFormat(data_dict, features_list, remove_all_zeroes = False, sort_keys = True)
labels, features = targetFeatureSplit(data)

# plot to see data point distribution
from data_vis import draw_data
draw_data(features_list, features, labels)



# check feature values
pois = dict([(x, y) for x, y in data_dict.items() if y["poi"] == True])
nons = dict([(x, y) for x, y in data_dict.items() if y["poi"] == False])

selected_feature = "total_payments"

for k, v in data_dict.items():
    if v[selected_feature] == "NaN": v[selected_feature] = 0
    
values_all = [y[selected_feature]\
            for x, y in data_dict.items()\
            if y[selected_feature] > 0]

print "person who has the highest {}: {}".format(\
    selected_feature, [x for x, y in data_dict.items() if y[selected_feature] == max(values_all)][0])

values_pois = [y[selected_feature]\
            for x, y in pois.items()\
            if y[selected_feature] > 0]

values_nons = [y[selected_feature]\
            for x, y in nons.items()\
            if y[selected_feature] > 0]

print "no. pois have {} = {}".format(\
    selected_feature, len(values_pois))
print "no. non-pois have {} = {}".format(\
    selected_feature, len(values_nons))

function_type = "mean"

print "{} {} of all insiders = {}".format(\
    function_type, selected_feature, np.mean(values_all))
print "{} {} of pois = {}".format(\
    function_type, selected_feature, np.mean(values_pois))
print "{} {} of non-pois = {}".format(\
    function_type, selected_feature, np.mean(values_nons))




