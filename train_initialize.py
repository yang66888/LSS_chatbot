from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import warnings

from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.sklearn_policy import SklearnPolicy



if __name__ == "__main__":
    # Apparently this method serves to verify if there are any mistakes on the NLU data file.
    utils.configure_colored_logging(loglevel = "DEBUG")

    training_data_file = "/Users/zhengyang/Desktop/working/storage_chatbot/data/stories.md"
    model_path = "/Users/zhengyang/Desktop/working/storage_chatbot/model_new/dialogue"

    # Class defined by Rasa that provides an interface to make use of training, handling messages, loading
    # dialog models etc.
    agent = Agent("chatbot_domain.yml", policies=[MemoizationPolicy(), KerasPolicy()])
    
    # Loads the training data on the path "./data/stories.md"
    training_data = agent.load_data(training_data_file)

    agent.train (
        training_data,
        # How many dummy stories should be created.
        augmentation_factor = 50,

        # 500 complete training cycles on the entire training dataset.
        epochs = 500,

        # The amount of training sample to use in eache pass. with this batch_size it will
        #take 50 epochs to go throw a entire dataset.
        batch_size = 10,

        # Percentage of data to validate the unbiase (imparcial) accuracy of a model.
        validation_split = 0.2
    )

    # Method used to persist a model into a directory for re-use.
    agent.persist(model_path)