#!/usr/bin/pickle

""" a basic script for importing student's POI identifier,
    and checking the results that they get from it 
 
    requires that the algorithm, dataset, and features list
    be written to my_classifier.pkl, my_dataset.pkl, and
    my_feature_list.pkl, respectively

    that process should happen at the end of poi_id.py
"""

import pickle
import sys
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.cross_validation import StratifiedShuffleSplit
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

import math

PERF_FORMAT_STRING = "\
\tAccuracy: {:>0.{display_precision}f}\
\n\tPrecision: {:>0.{display_precision}f}\tRecall: {:>0.{display_precision}f}\
\n\tF1: {:>0.{display_precision}f}\tF2: {:>0.{display_precision}f}"
RESULTS_FORMAT_STRING = "\tTotal folds: {:4d}\tTotal predictions: {:4d}\
\n\tTrue positives: {:4d}\tFalse positives: {:4d}\n\tFalse negatives: {:4d}\tTrue negatives: {:4d}"

PERF_FORMAT_STRING_ADDTL = "\
\tSensitivity: {:.5f}\tSpecificity: {:.5f}\
\n\tPositive likelihood: {:.5f}\tNegative likelihood: {:.5f}\
\n\tMatthews Cor: {:.5f}\tDiscrimination power: {:.5f}"

def model_scorer_base(clf, features, labels):
    cv = StratifiedShuffleSplit(labels, 500, random_state = 42)

    true_negatives = 0
    false_negatives = 0
    true_positives = 0
    false_positives = 0
    
    for train_idx, test_idx in cv: 
        features_train = []
        features_test  = []
        labels_train   = []
        labels_test    = []
        for ii in train_idx:
            features_train.append( features[ii] )
            labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
        
        ### fit the classifier using training set, and test on test set
        clf.fit(features_train, labels_train)
        predictions = clf.predict(features_test)
        
        for prediction, truth in zip(predictions, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            else:
                true_positives += 1
                
    return true_negatives, false_negatives, true_positives, false_positives

def model_scorer_harmony(clf, features, labels):
    true_negatives, false_negatives, true_positives, false_positives = model_scorer_base(clf, features, labels)
    #total_predictions = true_negatives + false_negatives + false_positives + true_positives
    #accuracy = 1.0*(true_positives + true_negatives)/total_predictions
    precision = 1.0*true_positives/(true_positives+false_positives) if (true_positives+false_positives) > 0 else 0.
    recall = 1.0*true_positives/(true_positives+false_negatives) if (true_positives+false_negatives) > 0 else 0.
    f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives) if (2*true_positives + false_positives+false_negatives) > 0 else 0.
    f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall) if (4*precision + recall) > 0 else 0.
    return f1 + f2


def test_classifier(clf, dataset, feature_list, folds = 1000):
    data = featureFormat(dataset, feature_list, sort_keys = True)
    labels, features = targetFeatureSplit(data)

    # default test_size=0.1
    cv = StratifiedShuffleSplit(labels, folds, random_state = 42)

    true_negatives = 0
    false_negatives = 0
    true_positives = 0
    false_positives = 0

    fold_counter = 0
    
    for train_idx, test_idx in cv: 
        features_train = []
        features_test  = []
        labels_train   = []
        labels_test    = []
        for ii in train_idx:
            features_train.append( features[ii] )
            labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
        
        fold_counter += 1
        ### fit the classifier using training set, and test on test set
        clf.fit(features_train, labels_train)
        predictions = clf.predict(features_test)
        for prediction, truth in zip(predictions, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            else:
                true_positives += 1
    try:
        total_predictions = true_negatives + false_negatives + false_positives + true_positives
        accuracy = 1.0*(true_positives + true_negatives)/total_predictions
        precision = 1.0*true_positives/(true_positives+false_positives)
        recall = 1.0*true_positives/(true_positives+false_negatives)
        f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
        f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall)
        sensitivity = 1.0*true_positives/(true_positives+false_negatives)
        specificity = 1.0*true_negatives/(true_negatives+false_positives)
        pos_like = sensitivity/(1 - specificity)
        neg_like = specificity/(1 - sensitivity)
        matt_cor = (true_positives*true_negatives - false_positives*false_negatives) \
                   /math.sqrt((true_positives + false_positives)* \
                              (true_positives + false_negatives)* \
                              (true_negatives + false_positives)* \
                              (true_negatives + false_negatives))
        disc_power = (math.sqrt(3)/math.pi)* \
                     (math.log(pos_like) + math.log(neg_like))
        print clf
        print PERF_FORMAT_STRING.format(accuracy, precision, recall, f1, f2, display_precision = 5)
        #print RESULTS_FORMAT_STRING.format(total_predictions, true_positives, false_positives, false_negatives, true_negatives)
        print PERF_FORMAT_STRING_ADDTL.format(sensitivity, specificity, \
                                              pos_like, neg_like, \
                                              matt_cor, disc_power)
    except:
        print "Got a divide by zero when trying out:", clf
        print ""
    print RESULTS_FORMAT_STRING.format(fold_counter, total_predictions, true_positives, false_positives, false_negatives, true_negatives)
    print ""


CLF_PICKLE_FILENAME = "my_classifier.pkl"
DATASET_PICKLE_FILENAME = "my_dataset.pkl"
FEATURE_LIST_FILENAME = "my_feature_list.pkl"

def dump_classifier_and_data(clf, dataset, feature_list):
    pickle.dump(clf, open(CLF_PICKLE_FILENAME, "w") )
    pickle.dump(dataset, open(DATASET_PICKLE_FILENAME, "w") )
    pickle.dump(feature_list, open(FEATURE_LIST_FILENAME, "w") )

def load_classifier_and_data():
    clf = pickle.load(open(CLF_PICKLE_FILENAME, "r") )
    dataset = pickle.load(open(DATASET_PICKLE_FILENAME, "r") )
    feature_list = pickle.load(open(FEATURE_LIST_FILENAME, "r"))
    return clf, dataset, feature_list

def main():
    ### load up student's classifier, dataset, and feature_list
    clf, dataset, feature_list = load_classifier_and_data()
    ### Run testing script
    test_classifier(clf, dataset, feature_list)

if __name__ == '__main__':
    main()
