#!/usr/bin/python

import pickle
import sys
sys.path.append("tools/")

from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn import decomposition, preprocessing

from email_preprocess import preprocess


use_new_feature, test_PCA = False, False
check_boundaries, check_k_folds = False, True
check_links = True
save_corpus_score = False


# check corpus stats
stats_handler = open("copus_stats.pkl", "r")
stats = pickle.load(stats_handler)
stats_handler.close()

print 'no. of email addresses used = ', len(stats)
total_email_cnt = sum(y["total"] for x, y in stats.items())
print 'no. of total emails sent = ', total_email_cnt
unique_email_cnt = sum(y["unique"] for x, y in stats.items())
print 'no. of unique emails sent = ', unique_email_cnt

# stemmed data generated by vectorize_text.py
keys_path = "corpus_features_from.pkl" 
features_path = "corpus_links_to.pkl"
labels_path = "corpus_labels.pkl"

print "features from", features_path


# get Tfidf vectorized features
keys, features, labels, names_scores = \
          preprocess(keys_path, features_path, labels_path, text_type="dict", \
                     max_doc_freq=1.0, min_doc_freq=1, select_percentile=100)

if check_links == True:
    links_handler = open("corpus_global_unique_links.pkl", "r")
    links = pickle.load(links_handler)
    links_handler.close()
    new_names_scores = []
    for t in names_scores:
        new_names_scores.append((t[0], links[int(t[1])], t[2]))
    names_scores = new_names_scores


# print to see some top feature names
top_features = sorted(names_scores, key=lambda x: x[2], reverse=True)[:10]

import pprint
pp = pprint.PrettyPrinter(indent=4)

print 'top scoring & features'
pp.pprint(top_features)


# extract feature names from the reference list
feature_names = [str(x[1]) for x in names_scores]

# PCA finding
if test_PCA == True:
    # scale data with mean = 0 and stdev = 1
    #features_scaled = preprocessing.scale(features)
    
    pca = decomposition.PCA(n_components=2)#n_components=4
    transformed = pca.fit_transform(features)
    #print pca.components_
    print pca.explained_variance_ratio_

    # plot to see PCA weights
    from data_vis import draw_PCA
    draw_PCA(transformed, pca.components_.T, feature_names, \
             arrow_size=2.5, text_pos=3.0)

data_dict = {}

for key, feature, label in zip(keys, features, labels):
    data_dict[key] = {"poi": label}
    data_dict[key].update(dict(zip(feature_names, feature)))

feature_names.insert(0, "poi")


# test with a variety of classifiers
if check_k_folds == True:
    from classifiers_testing import run_k_folds
    run_k_folds(data_dict, feature_names, folds=500, short=True)

# sum up ANOVA F-value stored in corpus_links_to.pk
# for each email comunication initiated by this address
# and save the total as corpus_score feature
if save_corpus_score == True:
    corpus_link_to_scores_dict = {}
    to_handler = open("corpus_features_to.pkl", "r")
    tos = pickle.load(to_handler)
    to_handler.close()
    for i in range(0, len(keys)):
        to_addrs = tos[i].split(" ")
        score = 0.
        for to_addr in to_addrs:
            for t in names_scores:
                if to_addr in t[1]:
                    score += t[2]
                    continue
        corpus_link_to_scores_dict[keys[i]] = {"corpus_score": score, "poi": labels[i]}
    pickle.dump(corpus_link_to_scores_dict, open("corpus_link_to_scores_dict.pkl", "w"))


from sklearn import cross_validation

features_train, features_test, labels_train, labels_test = \
                cross_validation.train_test_split(features, labels, test_size=0.1, random_state=42)

print "no. of features: training =", len(features_train), ", testing = ", len(features_test)
print "no. of labels: training =", len(labels_train), ", testing = ", len(labels_test)


from sklearn import tree

clf = tree.DecisionTreeClassifier()
clf.fit(features_train, labels_train)
pred = clf.predict(features_test)

from sklearn.metrics import accuracy_score

accuracy = accuracy_score(pred, labels_test)

print 'accuracy = ', accuracy

feature_importances = zip(clf.feature_importances_, feature_names[1:])
top_features = sorted(feature_importances, key=lambda x: x[0], reverse=True)[:10]

    
import pprint
pp = pprint.PrettyPrinter(indent=4)

print 'top {} importances & feature names'.format(10)
pp.pprint(top_features)



