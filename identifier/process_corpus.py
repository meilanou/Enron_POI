#!/usr/bin/python

import os
import pickle
import re
import sys
sys.path.append("tools/")
from sets import Set



from parse_out_email_text import parseOutText
from corpus_email_addresses import corpusDictByEmails
from learning_email_addresses import emailsForLearning

from datetime import datetime, date
months = {"Jan": 1,
          "Feb": 2,
          "Mar": 3,
          "Apr": 4,
          "May": 5,
          "Jun": 6,
          "Jul": 7,
          "Aug": 8,
          "Sep": 9,
          "Oct": 10,
          "Nov": 11,
          "Dec": 12}


corpus_dict_by_emails = corpusDictByEmails()
emails_for_learning = emailsForLearning()

corpus_features_date = []
corpus_features_subject = []
corpus_features_body = []
corpus_features_from = []
corpus_features_to = []
corpus_features_cc = []
corpus_features_bcc = []
corpus_labels = []
corpus_links_to = []
corpus_links_cc = []
corpus_links_bcc = []
corpus_links_all = []

corpus_global_unique_links = []
copus_stats = {}

# initiate with an impossible date
date_min, date_max = date(2100, 1, 1), date(1900, 1, 1)
date_inception = ()

# loop through all the email reference files
for email_address, info in corpus_dict_by_emails.items():

    # only process email addresses both exist in fin data and corpus
    # to reduce data amount, there are 86 addresses
    if not email_address in emails_for_learning: continue
    copus_stats[email_address] = {"total": 0, "unique": 0}
    
    # local variable for each reference file (multiple emails)
    subject_data, body_data = [], []
    timestamp_data = []
    to_emails_data, cc_emails_data, bcc_emails_data = [], [], []
    link_to_data, link_cc_data, link_bcc_data = {}, {}, {}
    
    # only focus on eamils from this address for personal writing style
    path_from = info["path_from"]
    is_poi = info["poi"]
    
    # record classification for this email address, POI or not
    corpus_labels.append(is_poi)

    # get all the email paths from the reference file
    email_paths = open(path_from, "r")

    # for each line of email path, parse content and receipients
    temp_counter = 0
    for path in email_paths:
        ### only look at first N emails when developing
        ### once everything is working, remove this line to run over full dataset
        #temp_counter += 1
        if temp_counter < 5:
            # increment unique email counter
            copus_stats[email_address]["total"] += 1
            
            path = os.path.join('..', path.replace("enron_mail_20110402/", "")[:-1])
            # skip if file doesn't exist
            if os.path.isfile(path) == False: continue
            email = open(path, "r")

            ### use parseOutText to extract the text and key info from the opened email
            timestamp, subject, to_emails, cc_emails, bcc_emails, body = parseOutText(email)

            # get standard email timestamp
            dt_elems = timestamp.split(" ")
            email_date = date(int(dt_elems[3]), months[dt_elems[2]], int(dt_elems[1]))
            if email_date < date_min: date_min = email_date
            elif email_date > date_max: date_max = email_date
            timestamp = email_date.strftime("%Y%m%d")
            
            # skip if it represent the same email
            if body in body_data:
                index = body_data.index(body)
                if subject_data[index] == subject and \
                   timestamp_data[index] == timestamp and \
                   len(set(to_emails_data[index]) - set(to_emails)) == 0 and \
                   len(set(cc_emails_data[index]) - set(cc_emails)) == 0 and \
                   len(set(bcc_emails_data[index]) - set(bcc_emails)) == 0:
##                   to_emails_data[index] == to_emails and \
##                   cc_emails_data[index] == cc_emails and \
##                   bcc_emails_data[index] == bcc_emails:
                    continue

            # increment unique email counter
            copus_stats[email_address]["unique"] += 1

            # 1 list of timestamp
            timestamp_data.append(timestamp)
            # 2 lists of text
            subject_data.append(subject)
            body_data.append(body)
            # 3 lists of email addresses
            to_emails_data.append(to_emails)
            cc_emails_data.append(cc_emails)
            bcc_emails_data.append(bcc_emails)
            # extracting linking information
            for to_email in to_emails:
                link_set = Set([email_address, to_email])
                if not link_set in corpus_global_unique_links: corpus_global_unique_links.append(link_set)
                key_i = str(corpus_global_unique_links.index(link_set))
                if not key_i in link_to_data.keys(): link_to_data[key_i] = 1
                else: link_to_data[key_i] += 1

            for cc_email in cc_emails:
                link_set = Set([email_address, cc_email])
                if not link_set in corpus_global_unique_links: corpus_global_unique_links.append(link_set)
                key_i = str(corpus_global_unique_links.index(link_set))
                if not key_i in link_cc_data.keys(): link_cc_data[key_i] = 1
                else: link_cc_data[key_i] += 1

            for bcc_email in bcc_emails:
                link_set = Set([email_address, bcc_email])
                if not link_set in corpus_global_unique_links: corpus_global_unique_links.append(link_set)
                key_i = str(corpus_global_unique_links.index(link_set))
                if not key_i in link_bcc_data.keys(): link_bcc_data[key_i] = 1
                else: link_bcc_data[key_i] += 1

            email.close()

    # record key info for this email address
    # make as space seperated string for vetorization
    corpus_features_date.append(" ".join(timestamp_data))
    corpus_features_subject.append(" ".join(subject_data))
    corpus_features_body.append(" ".join(body_data))
    corpus_features_from.append(email_address) # only one from email
    to_emails_data = " ".join(" ".join(map(str,l)) for l in to_emails_data)
    corpus_features_to.append(to_emails_data)
    cc_emails_data = " ".join(" ".join(map(str,l)) for l in cc_emails_data)
    corpus_features_cc.append(cc_emails_data)
    bcc_emails_data = " ".join(" ".join(map(str,l)) for l in bcc_emails_data)
    corpus_features_bcc.append(bcc_emails_data)
    corpus_links_to.append(link_to_data)
    corpus_links_cc.append(link_cc_data)
    corpus_links_bcc.append(link_bcc_data)
           
    email_paths.close()

print "no. of emails processed", len(corpus_labels)
print "dated from {} to {}".format(date_min, date_max)

##import pprint
##pp = pprint.PrettyPrinter(indent=4)
##pp.pprint(copus_stats)


pickle.dump(corpus_links_to, open("corpus_links_to.pkl", "w"))
pickle.dump(corpus_links_cc, open("corpus_links_cc.pkl", "w"))
pickle.dump(corpus_links_bcc, open("corpus_links_bcc.pkl", "w"))
pickle.dump(corpus_global_unique_links, open("corpus_global_unique_links.pkl", "w"))
pickle.dump(copus_stats, open("copus_stats.pkl", "w"))

pickle.dump(corpus_features_date, open("corpus_features_date.pkl", "w"))
pickle.dump(corpus_features_subject, open("corpus_features_subject.pkl", "w"))
pickle.dump(corpus_features_body, open("corpus_features_body.pkl", "w"))
pickle.dump(corpus_features_from, open("corpus_features_from.pkl", "w"))
pickle.dump(corpus_features_to, open("corpus_features_to.pkl", "w"))
pickle.dump(corpus_features_cc, open("corpus_features_cc.pkl", "w"))
pickle.dump(corpus_features_bcc, open("corpus_features_bcc.pkl", "w"))
pickle.dump(corpus_labels, open("corpus_labels.pkl", "w"))

# for full set
##pickle.dump(corpus_features_subject, open("corpus_features_subject_full.pkl", "w"))
##pickle.dump(corpus_features_body, open("corpus_features_body_full.pkl", "w"))
##pickle.dump(corpus_features_to, open("corpus_features_from_full.pkl", "w"))
##pickle.dump(corpus_features_to, open("corpus_features_to_full.pkl", "w"))
##pickle.dump(corpus_features_cc, open("corpus_features_cc_full.pkl", "w"))
##pickle.dump(corpus_features_bcc, open("corpus_features_bcc_full.pkl", "w"))
##pickle.dump(corpus_labels, open("corpus_labels_full.pkl", "w"))


