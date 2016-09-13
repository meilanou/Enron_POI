#!/usr/bin/python

import pickle
import sys
sys.path.append("tools/")
import math
import numpy as np

from feature_format import featureFormat, targetFeatureSplit
from corpus_email_addresses import corpusDictByEmails

learning_only = True

### Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','count_from','count_to']

# final_project_dataset.pkl has 146 keys
# final_project_dataset_modified.pkl has 143 keys
data_dict = corpusDictByEmails()


if learning_only == True:
    from learning_email_addresses import emailsForLearning
    learning_email_addr_list = emailsForLearning()
    data_dict = dict([(x, y) for x, y in data_dict.items() if x in learning_email_addr_list])


print "no. total available features =", len(data_dict[data_dict.keys()[0]])

pois = dict([(x, y) for x, y in data_dict.items() if y["poi"] == True])
nons = dict([(x, y) for x, y in data_dict.items() if y["poi"] == False])

print "no. of POIs =", len(pois)
print "no. of non-POIs =", len(nons)

import pprint
pp = pprint.PrettyPrinter(indent=4)

max_from = max([y["count_from"] for x, y in pois.items()])
print "POI sent the highest number of emails:"
pp.pprint([(x, y) for x, y in pois.items() if y["count_from"] == max_from])
max_to = max([y["count_to"] for x, y in pois.items()])
print "POI received the highest number of emails:"
pp.pprint([(x, y) for x, y in pois.items() if y["count_to"] == max_to])

### Remove outliers, if needed
#data_dict.pop('TOTAL', 0)
#data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)

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
draw_data(features_list, features, labels, filename="data.png")

### check feature values
##pois = dict([(x, y) for x, y in data_dict.items() if y["poi"] == True])
##nons = dict([(x, y) for x, y in data_dict.items() if y["poi"] == False])
##
##selected_feature = "total_payments"
##
##for k, v in data_dict.items():
##    if v[selected_feature] == "NaN": v[selected_feature] = 0
##    
##values_all = [y[selected_feature]\
##            for x, y in data_dict.items()\
##            if y[selected_feature] > 0]
##
##print "person who has the highest {}: {}".format(\
##    selected_feature, [x for x, y in data_dict.items() if y[selected_feature] == max(values_all)][0])
##
##values_pois = [y[selected_feature]\
##            for x, y in pois.items()\
##            if y[selected_feature] > 0]
##
##values_nons = [y[selected_feature]\
##            for x, y in nons.items()\
##            if y[selected_feature] > 0]
##
##print "no. pois have {} = {}".format(\
##    selected_feature, len(values_pois))
##print "no. non-pois have {} = {}".format(\
##    selected_feature, len(values_nons))
##
##function_type = "mean"
##
##print "{} {} of all insiders = {}".format(\
##    function_type, selected_feature, np.mean(values_all))
##print "{} {} of pois = {}".format(\
##    function_type, selected_feature, np.mean(values_pois))
##print "{} {} of non-pois = {}".format(\
##    function_type, selected_feature, np.mean(values_nons))




