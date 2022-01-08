# https://analyticsindiamag.com/guide-to-named-entity-recognition-with-spacy-and-nltk/

import spacy
import pandas as pd
import os


def read_text_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        raw_text = f.read()
    return raw_text


# function to get unique values
def unique(list1):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            x = x.replace("'s", "")
            x = x.replace("]", "")
            x = x.strip()
            unique_list.append(x)
    return unique_list


path_to_files = 'C:\\Users\\mmocak\\PycharmProjects\\pythonLearning\\PythonWebScraping\\webofstories_beautifulSoup\\stories\\test'
# path_to_file = 'stories/john-wheeler.txt'
#path_to_files = 'stories\\test'


os.chdir(path_to_files)

# create empty final dataframe
data = {'Source': [''], 'Target': ['']}
df = pd.DataFrame(data)
df_final = df

# iterate through all file
for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".txt"):
        file_path = f"{path_to_files}\{file}"
        print(file_path)

        # call read text file function
        raw_text = read_text_file(file_path)

        # this is required to run from terminal > python -m spacy download en_core_web_sm
        NER = spacy.load("en_core_web_sm", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])

        text = NER(raw_text)

        people = []
        for w in text.ents:
            if w.label_ == 'PERSON':
                # print(w.text,w.label_)
                people.append(w.text)

        unique_people = unique(people)

        source_person = []
        for i in range(len(unique_people)):
            source_person.append(unique_people[0])

        # assign data of lists.
        data = {'Source': source_person, 'Target': unique_people}

        # Create DataFrame.
        df = pd.DataFrame(data)

    df_final = df_final.append(df)

# Print the output.
# print(df_final)

df_final.to_pickle("a_file.pkl")


# for w in text.ents:
#    if w.label_ == 'ORG':
#        print(w.text)
