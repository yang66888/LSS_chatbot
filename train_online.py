from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core import utils, train
from rasa_core.training import online
from rasa_core.interpreter import NaturalLanguageInterpreter

logger = logging.getLogger(__name__)

def train_agent(interpreter):
    return train.train_dialogue_model(domain_file = "/Users/zhengyang/Desktop/working/storage_chatbot/chatbot_domain.yml",
                                        stories_file = "/Users/zhengyang/Desktop/working/storage_chatbot/data/stories.md",
                                        output_path = "./model_new/dialogue",
                                        nlu_model_path = interpreter,
                                        endpoints="/Users/zhengyang/Desktop/working/storage_chatbot/endpoints.yml",
                                        max_history = 2,
                                        kwargs = {"batch_size" : 50,
                                                "epochs" : 200,
                                                "max_training_samples": 300
                                                })

if __name__ == "__main__":
    utils.configure_colored_logging(loglevel = "DEBUG")
    nlu_model_path = "./model_new/nlu/default/LSS_chatbot"
    interpreter = NaturalLanguageInterpreter.create(nlu_model_path)
    agent = train_agent(interpreter)
    online.serve_agent(agent)