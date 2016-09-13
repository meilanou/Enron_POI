#!/usr/bin/python

import pickle
import numpy as np

print "\n=== From Finance Data ===\n"

fin_data_dict = pickle.load(open("final_project_dataset.pkl", "r") )
# notice I already know to remove TOTAL
fin_data_dict.pop('TOTAL', 0)

pois_fin = dict([(x, y) for x, y in fin_data_dict.items() if y["poi"] == True])
nons_fin = dict([(x, y) for x, y in fin_data_dict.items() if y["poi"] == False])

print 'no. total pois =', len(pois_fin.keys())
print 'no. total non-pois =', len(nons_fin.keys())

selected_feature = "email_address"

print "no. of pois have {} = {}".format(\
    selected_feature, len(\
        [x for x, y in pois_fin.items() \
         if y[selected_feature] != "NaN"]))
print "no. of non-pois have {} = {}".format(\
    selected_feature, len(\
        [x for x, y in nons_fin.items() \
         if y[selected_feature] != "NaN"]))

print "\n=== From Manual Email List ===\n"

from poi_email_addresses import poiEmails, poiDictByEmails, poiDictByNames

poi_emails = poiEmails()
poi_dict_emails = poiDictByEmails()
poi_dict_names = poiDictByNames()

print "no. total poi emails provided =", len(poi_emails)
print "no. total pois associated to emails provided =", len(poi_dict_names)

print "\n=== From Email Corpus Reference Files ===\n"

from corpus_email_addresses import corpusDictByEmails

corpus_dict_emails = corpusDictByEmails()

pois_cor = dict([(x, y) for (x, y) in corpus_dict_emails.items() if y["poi"] == True])
nons_cor = dict([(x, y) for (x, y) in corpus_dict_emails.items() if y["poi"] == False])

print 'no. total unique emails =', len(corpus_dict_emails.keys())
print 'no. total pois =', len(pois_cor.keys())
print 'no. total emails from pois =', \
      sum([y["count_from"] for x, y in pois_cor.items()])
print 'no. total missing emails from pois =', \
      sum([y["count_from_missing"] for x, y in pois_cor.items()])
print 'no. total emails to pois =', \
      sum([y["count_to"] for x, y in pois_cor.items()])
print 'no. total missing emails to pois =', \
      sum([y["count_to_missing"] for x, y in pois_cor.items()])
print 'no. total non-pois =', len(nons_cor.keys())
print 'no. total emails from non-pois =', \
      sum([y["count_from"] for x, y in nons_cor.items()])
print 'no. total missing emails from non-pois =', \
      sum([y["count_from_missing"] for x, y in nons_cor.items()])
print 'no. total emails to non-pois =', \
      sum([y["count_to"] for x, y in nons_cor.items()])
print 'no. total missing emails to non-pois =', \
      sum([y["count_to_missing"] for x, y in nons_cor.items()])

print "\n=== Cross Checking ===\n"

pois_fin_emails = [y["email_address"] for (x, y) in pois_fin.items() if y["email_address"] != "NaN"]
pois_cor_emails = pois_cor.keys()

print "no. of poi emails in both fin data and list =", \
      len(set(poi_emails) & set(pois_fin_emails))
print "no. of poi emails in both corpus and list =", \
      len(set(poi_emails) & set(pois_cor_emails))

print "no. of poi emails in both fin data and corpus =", \
      len(set(pois_fin_emails) & set(pois_cor_emails))

import pprint
pp = pprint.PrettyPrinter(indent=4)

print "poi emails in fin data NOT in corpus"
pp.pprint(sorted(set(pois_fin_emails) - set(pois_cor_emails)))
print "poi emails in corpus NOT in fin data"
pp.pprint(sorted(set(pois_cor_emails) - set(pois_fin_emails)))

nons_fin_emails = [y["email_address"] for (x, y) in nons_fin.items() if y["email_address"] != "NaN"]
nons_cor_emails = nons_cor.keys()

print "no. of non-poi emails in both fin data and corpus =", \
      len(set(nons_fin_emails) & set(nons_cor_emails))

# cross checking if manual mapping of poi emails to poi names is all correct
poi_name_emil_matches = {}

for (x, y) in pois_fin.items():
    poi_name = x
    poi_email = y["email_address"]
    if poi_email in poi_dict_emails:
        if poi_dict_emails[poi_email] == poi_name:
            poi_name_emil_matches[poi_name] = poi_email

print "no. of poi emails and names mapped in fin data and list =", \
      len(poi_name_emil_matches)

