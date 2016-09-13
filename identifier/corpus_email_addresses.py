#!/usr/bin/python

def corpusDictByEmails():
    pickle_path = "corpus_dict_by_emails.pkl"

    
    from os.path import isfile
    import pickle

    if isfile(pickle_path):
    
        file_handler = open(pickle_path, "r")
        data_dict = pickle.load(file_handler)
        file_handler.close()

    else:
        
        from os import listdir
        from os.path import join, isfile
        import re
        
        from poi_email_addresses import poiEmails
        poi_email_list = poiEmails()

        emails_by_address_path = "emails_by_address/"
        # get the list of filenames of all files in this directory
        emails_by_address_files = [f for f in listdir(emails_by_address_path)]
                                  # if isfile(join(emails_by_address_path, f))

        data_dict = {}

        for filename in emails_by_address_files:
            # filename is consist of direction, email and extension
            # e.g. from_alan.larsen@enron.com.txt
            elems = re.split("_|.txt", filename, maxsplit=2)
            isFrom = True if elems[0] == "from" else False
            email = elems[1]
            isPOI = True if email in poi_email_list else False
            filePath = join(emails_by_address_path, filename)

            if email not in data_dict:
                data_dict[email] = {"count_from": 0,
                                    "count_to": 0,
                                    "poi": isPOI,
                                    "path_from": "NaN",
                                    "path_to": "NaN"}

            # each txt file contains lines of paths to actual emails
            list_doc = open(filePath, "r")
            # count the number of lines of email paths
            # each line represents the path to one email
            num_lines = 0
            num_lines_missing = 0
            for path in list_doc:
                path = join('..', path.replace("enron_mail_20110402/", "")[:-1])
                if isfile(path) == True: num_lines += 1
                else: num_lines_missing += 1
            list_doc.close()
            
            # log path to this file and number of emails for the direction
            if isFrom == True:
                data_dict[email]["count_from"] = num_lines
                data_dict[email]["count_from_missing"] = num_lines_missing
                data_dict[email]["path_from"] = filePath
            else:
                data_dict[email]["count_to"] = num_lines
                data_dict[email]["count_to_missing"] = num_lines_missing
                data_dict[email]["path_to"] = filePath

        pickle.dump(data_dict, open(pickle_path, "w"))

    return data_dict
