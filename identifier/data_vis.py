#!/usr/bin/python


import matplotlib 
#matplotlib.use('agg')

import matplotlib.pyplot as plt
import seaborn as sns
import pylab as pl
import numpy as np

from os import path
d = path.dirname(__file__)

c_red = "#CF2913"
c_blue = "#3C3CA6"


def draw_PCA(transformed_features, feature_vectors, features_list, \
             arrow_size=5.0, text_pos=5.5):   
    plt.figure(figsize=(12, 8))
    sns.regplot(transformed_features[:, 0], transformed_features[:, 1], fit_reg=False)

    for i, v in enumerate(feature_vectors):
        plt.arrow(0, 0, arrow_size*v[0], arrow_size*v[1], 
                  head_width=0.05, head_length=0.1)
        plt.text(v[0]*text_pos, v[1]*text_pos, features_list[i], color='r', 
                 ha='center', va='center', fontsize=16)
        
    plt.xlabel("PC1", fontsize=14)
    plt.ylabel("PC2", fontsize=14)
    plt.title("PC plane with feature projections.", fontsize=18)
    plt.show()

def draw_data(selections, features, labels, weight=False, filename="data.png"):       
    poi_x = [features[ii][0] for ii in range(0, len(features)) if labels[ii]==1]
    poi_y = [features[ii][1] for ii in range(0, len(features)) if labels[ii]==1]
    non_x = [features[ii][0] for ii in range(0, len(features)) if labels[ii]==0]
    non_y = [features[ii][1] for ii in range(0, len(features)) if labels[ii]==0]

    no_total = len(labels)
    no_poi = len(poi_x)
    no_non = len(non_x)
    
    plt.scatter(poi_x, poi_y, c=c_red, \
                label="{0}(poi)/{1}".format(no_poi, no_total), \
                s=200, alpha=0.5)
    plt.scatter(non_x, non_y, c=c_blue, \
                label="{0}(not)/{1}".format(no_non, no_total), \
                s=200, alpha=0.5)
    plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left", borderaxespad=0.)

    plt.xlabel(selections[1])
    plt.ylabel(selections[2])
        
    #plt.savefig(filename)
    plt.show()
    
def draw_cluster(pred, features, labels, mark_poi=False, \
                filename="cluster.png", f1_name="feature 1", f2_name="feature 2"):
    """ some plotting code designed to help you visualize your clusters """

    ### plot each cluster with a different color--add more colors for
    ### drawing more than 4 clusters
    colors = ["b", "m", "c", "k", "g"]
    for ii, pp in enumerate(pred):
        plt.scatter(features[ii][0], features[ii][1], color = colors[pred[ii]])

    ### if you like, place red stars over points that are POIs (just for funsies)
    if mark_poi:
        for ii, pp in enumerate(pred):
            if labels[ii]:
                plt.scatter(features[ii][0], features[ii][1], color="r", \
                            marker="*")
    plt.xlabel(f1_name)
    plt.ylabel(f2_name)
    plt.savefig(filename)
    plt.show()
    
def draw_classifier(clf, selections, features, labels, filename="class.png"):
    x_min = 0.0; x_max = 1.0
    y_min = 0.0; y_max = 1.0

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, m_max]x[y_min, y_max].
    h = .01  # step size in the mesh
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    #plt.xlim(xx.min(), xx.max())
    #plt.ylim(yy.min(), yy.max())

    #plt.pcolormesh(xx, yy, Z, cmap=pl.cm.seismic)
    #print features[0:10]
    #print labels[0:10]
    # Plot also the test points
    if selections[0] == "poi":
        index_x = selections[1]; index_y = selections[2]
    else:
        index_x = 0; index_y = 1
        
    poi_x = [features[ii][0] for ii in range(0, len(features)) if labels[ii]==1]
    poi_y = [features[ii][1] for ii in range(0, len(features)) if labels[ii]==1]
    non_x = [features[ii][0] for ii in range(0, len(features)) if labels[ii]==0]
    non_y = [features[ii][1] for ii in range(0, len(features)) if labels[ii]==0]
        
    plt.scatter(poi_x, poi_y, color = "r", label="poi")
    plt.scatter(non_y, non_y, color = "b", label="non-poi")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    plt.xlabel(selections[1])
    plt.ylabel(selections[2])

    plt.savefig(filename)
    plt.show()
    
import base64
import json
import subprocess

def output_image(name, format, bytes):
    image_start = "BEGIN_IMAGE_f9825uweof8jw9fj4r8"
    image_end = "END_IMAGE_0238jfw08fjsiufhw8frs"
    data = {}
    data['name'] = name
    data['format'] = format
    data['bytes'] = base64.encodestring(bytes)
    print image_start+json.dumps(data)+image_end
