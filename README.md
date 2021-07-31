# This is Dissertation project 

## Project Description: 

A chatbot is a software application used to conduct an on-line chat conversation via text in lieu of providing direct contact with a human agent. Chatbot technology has evolved with the introduction of natural language processing and machine learning techniques. It is a great approach to reduce labor cost and improve customer satisfaction by providing 24x7 reliable and fast customer support. 
This research project is to develop a Chatbot model for LSS (Local Student Storage) using NLP algorithms. The model is designed to handle most frequently asked questions from customers, based on over 20,000 previous email exchanges. The system will recognize customer’s intents, handle conversation state, utterances, actions, and generate responses to the customer. The chatbot has been validated and is ready to be commercialized.

## Files/folders contained in this project: 

- folder data where metadata is saved which contains data.json(original data), training_data.json(80% of original data for training purposes), test_data(20% of original data for validation), datanew.json(new data with intents combined), training_data_new(80% of new data for training purposes),test_data_new(80% of new data for training purposes),storied.md 
- folder model: dialogue where training policies sit and nlu where intent classifier and evaluation result sit.
- train_initialize.py
- train_online.py
- visualization.py
- chatbot_domain.yml 
- endpoints.yml 
- graph.png(system visualisation) 
- actions.py(customised actions)
- rasa_core.log 
- rasa_core where sits neural network model for reinforcement learning
- pycache + action_app (for chatbot implementation purposes) 
