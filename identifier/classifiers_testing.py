#!/usr/bin/pickle


# Code derived from
# http://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB

classifiers = [
    ("Naive Bayes",GaussianNB()),
    #("Linear SVM", SVC(kernel="linear", C=0.25)),
    ("RBF SVM", SVC(gamma=2, C=1)),
    ("Decision Tree",DecisionTreeClassifier(max_depth=5)),
    ("Nearest Neighbors", KNeighborsClassifier(3)),
    ("Random Forest", RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)),
    ("AdaBoost", AdaBoostClassifier())]

fold_count = -((-len(classifiers) - 1)//2)

classifiers_short = [
    ("Naive Bayes",GaussianNB()),
    ("RBF SVM", SVC(gamma=2, C=1)),
    ("Decision Tree",DecisionTreeClassifier(max_depth=5)),
    ("Nearest Neighbors", KNeighborsClassifier(3))]

def run_k_folds(data_dict, features_list, folds=1000, short=False):
    from tester import test_classifier

    if short == True:
        cl_list = classifiers_short
    else:
        cl_list = classifiers
        
    for name, clf in cl_list:
        print name
        test_classifier(clf, data_dict, features_list, folds=folds)
##        if name == "Decision Tree":
##            # find most important features
##            features_only = features_list[1:]
##            top_count = 10 if len(features_only) > 10 else len(features_only)
##            feature_importances = zip(clf.feature_importances_, features_only)
##            tops = sorted(feature_importances, key=lambda x: x[0], reverse=True)[:top_count]
##
##            import pprint
##            pp = pprint.PrettyPrinter(indent=4)
##
##            print 'top {} importances & feature names'.format(top_count)
##            pp.pprint(tops)



def plot_boundaries(data_dict, features_list, step_size, test_size=0.1):
    from feature_format import featureFormat, targetFeatureSplit
    data = featureFormat(data_dict, features_list[:3]) # only need poi and first 2 features
    labels, features = targetFeatureSplit(data)

    figure = plt.figure(figsize=(20, 10))

    # preprocess dataset, split into training and test part
    features_train, features_test, labels_train, labels_test = \
                    train_test_split(features, labels, test_size=test_size, random_state=42)

    points_x = [features[ii][0] for ii in range(0, len(features))]
    points_y = [features[ii][1] for ii in range(0, len(features))]
    
    x_min, x_max = min(points_x) - step_size, max(points_x) + step_size
    y_min, y_max = min(points_y) - step_size, max(points_y) + step_size
    xx, yy = np.meshgrid(np.arange(x_min, x_max, step_size),
                         np.arange(y_min, y_max, step_size))

    train_x = [features_train[ii][0] for ii in range(0, len(features_train))]
    train_y = [features_train[ii][1] for ii in range(0, len(features_train))]
    test_x = [features_test[ii][0] for ii in range(0, len(features_test))]
    test_y = [features_test[ii][1] for ii in range(0, len(features_test))]

    # just plot the dataset first
    cm = plt.cm.seismic
    cm_bright = ListedColormap(['#0000FF','#FF0000'])
    ax = plt.subplot(2, fold_count, 1)
    # Plot the training points
    ax.scatter(train_x, train_y, c=labels_train, cmap=cm_bright)
    # and testing points
    ax.scatter(test_x, test_y, c=labels_test, cmap=cm_bright, alpha=0.6)
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    #ax.set_xticks(())
    #ax.set_yticks(())

    # iterate over classifiers
    i = 2
    for name, clf in classifiers:
        ax = plt.subplot(2, fold_count, i)
        clf.fit(features_train, labels_train)
        score = clf.score(features_test, labels_test)
        # Plot the decision boundary. For that, we will assign a color to each
        # point in the mesh [x_min, m_max]x[y_min, y_max].
        if hasattr(clf, "decision_function"):
            Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
        else:
            Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)
        # Plot also the training points
        ax.scatter(train_x, train_y, c=labels_train, cmap=cm_bright)
        # and testing points
        ax.scatter(test_x, test_y, c=labels_test, cmap=cm_bright, alpha=0.6)
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        #ax.set_xticks(())
        #ax.set_yticks(())
        ax.set_title(name)
        ax.text(xx.max() - .3, yy.min() + .3, ('%.2f' % score).lstrip('0'),
                size=15, horizontalalignment='right')
        i += 1

    figure.subplots_adjust(left=.02, right=.98)
    plt.show()

