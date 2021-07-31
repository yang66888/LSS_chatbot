# Import&Clean data

import mailbox
import email
from email.policy import default
import pandas as pd
import numpy as np

# Define a function to import mbox file 
# Getting plain text 'email body'
def getbody(message): #getting plain text 'email body'
    body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload()
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload()
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload()
    
    return body

# Convert mbox into pandas dataframe 
MBOX = '/Users/zhengyang/Documents/Takeout/Mail/all_mail.mbox'
mbox = mailbox.mbox(MBOX)

mbox_dict = {}
for i, msg in enumerate(mbox):
    mbox_dict[i] = {}
    for header in msg.keys():
        mbox_dict[i][header] = msg[header]
    mbox_dict[i]['Body'] = getbody(msg)
    
df = pd.DataFrame.from_dict(mbox_dict, orient='index')

# Remove non-essential columns
cols_to_keep = ['From', 'To', 'Cc', 'Bcc', 'Subject', 'Body']
df = df[cols_to_keep]

# Clean data 
def clean(x):
    x = re.sub(r'www.*$', '', x)
    x = re.sub('\S+@\S+(?:\.\S+)+', '', x)
    x = re.sub(r'Local Student Storage:*$', '', x)
    x = re.sub('<.*?>', '', x)
    x = re.sub('>20', '', x)
    x = re.sub('wrote', '', x)
    x = re.sub('Jacqueline Heal', '', x)
    x = re.sub('Best wishes,', '', x) 
    x = re.sub('[^:.,!?a-zA-Z0-9 \n\.]', '', x)
    x = re.sub('E28099', "'", x)
    return x

# Build System

from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Interpreter


# Define training function
def train_chabot(data_json, config_file, model_dir):
    training_data = load_data(data_json)
    trainer = Trainer(config.load(config_file))
    trainer.train(training_data)
    model_directory = trainer.persist(model_dir, fixed_model_name = 'LSS_chatbot')

# Define predict function 
def predict_intent(text):
    interpreter = Interpreter.load('/Users/zhengyang/Desktop/working/storage_chatbot/model_new/nlu/default/LSS_chatbot')
    print(interpreter.parse(text))

##Evaluation 

#Split data into training data and test data

import os
import pandas as pd
import matplotlib.pyplot as plt
from rasa_nlu.model import Trainer
from rasa_nlu.evaluate import run_evaluation
from rasa_nlu import config
from rasa_nlu.training_data import load_data
import random
import time

"""
Function to sample the training and test examples from the list of examples
initial_data is a dataframe composed of the list of all examples we want to sample from
nb_of_examples is the number of examples we want for both training and testing
"""

# if too many examples asked to take all the examples and divided them in 20% 80%
def select_examples(initial_data, nb_of_examples):
    if nb_of_examples > len(initial_data["rasa_nlu_data"]["common_examples"]):
        nb_of_examples = len(initial_data["rasa_nlu_data"]["common_examples"])
   # list of examples for training data
    training_examples_list = []
   # list of examples for test data
    test_examples_list = []
   # copy the examples dataframe to remove select directly the rows to keep for training and test
    training_df = initial_data.copy()
    test_df = initial_data.copy()
   # Dataframe of examples
    examples_df = pd.DataFrame.from_records(initial_data["rasa_nlu_data"]["common_examples"])
   # a series that contains for each intent the percentage of examples
    serie_distOfExamples = examples_df["intent"].value_counts()/len(examples_df)
    # n is the number of examples for intent to keep: for both training and testing
    for intent in serie_distOfExamples.index.values:
        n=int(serie_distOfExamples[intent]*nb_of_examples)
       # the list of indexes for "intent" in the dataframe
        l = examples_df[examples_df["intent"] == intent].index.values
       # select randomly n indexes in l
        examples_samp = random.sample(list(l),n)
       # 80% of those examples are kept for training
        training_examples_ids = random.sample(examples_samp,int(n*0.8))
       # the rest is for testing
        for ex_id in training_examples_ids:
            examples_samp.remove(ex_id)
        for index_train in training_examples_ids:
            training_examples_list.append(initial_data["rasa_nlu_data"]["common_examples"][index_train])
        for index_test in examples_samp:
            test_examples_list.append(initial_data["rasa_nlu_data"]["common_examples"][index_test])
   # we replace for both training and testing df the corresponding intent rows by the one we selected
    training_df["rasa_nlu_data"]["common_examples"] = training_examples_list
    test_df["rasa_nlu_data"]["common_examples"] = test_examples_list

    return training_df, test_df

# Define a function to reconstruct the JSON file for training and test examples from the output of the previous method
def construct_jsonExampleFile(training_df, test_df, initial_data):
    training_df.to_json('/Users/zhengyang/Desktop/working/storage_chatbot/data1/training_data_new.json')
    test_df.to_json('/Users/zhengyang/Desktop/working/storage_chatbot/data1/test_data_new.json')

# Define a function to evaluate model

def evaluateModel1(pathToData,model_dir):
    path_to_data = "/Users/zhengyang/Desktop/working/storage_chatbot/data/new_data.json"

    # Create a directory if not exist.
    if not os.path.exists(model_dir +"/evaluation1"):
        os.mkdir(model_dir +"/evaluation1")
        print("Directory ", "evaluation1", " Created ")

    # save the error file, Confusion matrix image, and histogram file
    errors_path = model_dir + "/evaluation1/errors.json"
    confmat_path = model_dir + "/evaluation1/confmat"
    intent_hist_path = model_dir + "/evaluation1/hist"
    run_evaluation(path_to_data, model_dir, errors_filename=errors_path, confmat_filename=confmat_path,
                   intent_hist_filename=intent_hist_path)







