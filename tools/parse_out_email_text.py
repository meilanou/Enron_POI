#!/usr/bin/python

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer('english')
import string
import re

def parseOutText(f):
    """ given an opened email file f, parse out:
        1) subject, stemmed
        2) receipients (to, cc, bcc)
        3) all text below the metadata block, stemmed 
        
        """

    f.seek(0)  ### go back to beginning of file (annoying)
    all_text = f.read()

    # for checking purpose
    timestamp = ""
    # 5 key items
    subject = ""
    body = ""
    to_emails = []
    cc_emails = []
    bcc_emails = []
    
    ### split off content
    elems = all_text.split("X-FileName:")
    
    # only process email that has both metadata and body
    if len(elems) > 1:
        metadata = elems[0]
        body = elems[1]
    
        ### split off metadata
        elems = metadata.split("X-From:")
        if len(elems) > 1:
            metadata_raw = elems[0]
            metadata_X = elems[1]

            delimiters = []
            has_to, has_cc, has_bcc = False, False, False

            # key items beside email subject body, all optional
            has_to = "To: " in metadata_raw
            has_cc = "Cc: " in metadata_raw
            has_bcc = "Bcc: " in metadata_raw

            elems = re.split("Date:|From:", metadata_raw)
            timestamp = elems[1].strip()

            # extract data by item type, all treated as string to vectorization
            elems = re.split("Subject:|Cc:" if has_cc == True else "Subject:|Mime-Version:", metadata_raw)
            subject = elems[1].strip()
                
            if has_to == True:
                elems = re.split("To:|Subject:", metadata_raw)
                to_emails = elems[1].translate(None, '\n\t ').split(",")
            if has_cc == True:
                elems = re.split("Cc:|Mime-Version:", metadata_raw)
                cc_emails = elems[1].translate(None, '\n\t ').split(",")
            if has_bcc == True:
                elems = re.split("Bcc:|X-From:", metadata_raw)
                bcc_emails = elems[1].translate(None, '\n\t ').split(",")

    # only process if there is any word
    if len(body) > 0:
        body = stemWords(body)

    if len(subject) > 0:
        subject = stemWords(subject)

    if len(to_emails) == 0: to_emails = ['NA']
    if len(cc_emails) == 0: cc_emails = ['NA']
    if len(bcc_emails) == 0: bcc_emails = ['NA']

                    
    return timestamp, subject, to_emails, cc_emails, bcc_emails, body

   
def stemWords(text):

    
    ### remove punctuation
    text = text.translate(string.maketrans("", ""), string.punctuation)

    ### split the text string into individual words, stem each word,
    ### and append the stemmed word to words (make sure there's a single
    ### space between each stemmed word)
    #stemmer = SnowballStemmer('english')

    words = ""
    for w in text.split():
        words += stemmer.stem(w) + ' '

    return words.strip()
        
##def main():
##    ff = open("../text_learning/test_email.txt", "r")
##    text = parseOutText(ff)
##    print text

##if __name__ == '__main__':
##    main()

