#!/usr/bin/python


def emailsForLearning():
    """
    only process email addresses both exist in fin data and corpus
    to reduce data amount, there are 86 addresses
    """
    pickle_path = "emails_for_learning.pkl"

    from os.path import isfile
    import pickle

    if isfile(pickle_path):
        
        file_handler = open(pickle_path, "r")
        emails = pickle.load(file_handler)
        file_handler.close()

        return emails

    else:

        # load financial data
        fin_data_dict = pickle.load(open("final_project_dataset.pkl", "r") )
        # notice I already know to remove TOTAL
        fin_data_dict.pop('TOTAL', 0)

        pois_fin = dict([(x, y) for x, y in fin_data_dict.items() if y["poi"] == True])
        nons_fin = dict([(x, y) for x, y in fin_data_dict.items() if y["poi"] == False])

        from corpus_email_addresses import corpusDictByEmails

        corpus_dict_emails = corpusDictByEmails()

        pois_cor = dict([(x, y) for (x, y) in corpus_dict_emails.items() if y["poi"] == True])
        nons_cor = dict([(x, y) for (x, y) in corpus_dict_emails.items() if y["poi"] == False])

        pois_fin_emails = [y["email_address"] for (x, y) in pois_fin.items() if y["email_address"] != "NaN"]
        pois_cor_emails = pois_cor.keys()

        poi_emails_for_learning = list(set(pois_fin_emails) & set(pois_cor_emails))

        nons_fin_emails = [y["email_address"] for (x, y) in nons_fin.items() if y["email_address"] != "NaN"]
        nons_cor_emails = nons_cor.keys()

        non_emails_for_learning = list(set(nons_fin_emails) & set(nons_cor_emails))

        emails = poi_emails_for_learning + non_emails_for_learning
        pickle.dump(emails, open(pickle_path, "w"))

        return emails



