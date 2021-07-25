# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"
import smtplib
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.executor import CollectingDispatcher
import os
from haystack.document_store import FAISSDocumentStore
from haystack.reader.farm import FARMReader
from haystack.utils import print_answers
from haystack.retriever.sparse import TfidfRetriever
from haystack.pipeline import ExtractiveQAPipeline
from haystack.file_converter.txt import TextConverter
#from haystack.file_converter.pdf import PDFToTextConverter
#from haystack.file_converter.docx import DocxToTextConverter
from haystack.preprocessor.preprocessor import PreProcessor
from email.mime.text import MIMEText
from tensorflow import keras
import tensorflow_hub as hub
from rasa_sdk.forms import FormValidationAction
from spacy import displacy
import json
import re
import en_core_web_md
nlp = en_core_web_md.load()
from rasa_sdk.events import SlotSet, FollowupAction
import requests
import os
import asyncio

import websockets
#from rocketchat.api import RocketChatAPI
#from requests.auth import HTTPBasicAuth 

class ActionCreateDirectMessage(Action):
#
    def name(self) -> Text:
        return "action_create_direct_message"

    async def hello(self):
        uri = "ws://rocketchat:3000/websocket"
        async with websockets.connect(uri) as rocketChatSocket:
            # Receive ack
            await rocketChatSocket.recv()

            connectRequest = {
                "msg": "connect",
                "version": "1",
                "support": ["1", "pre2", "pre1"]
            }
            await rocketChatSocket.send(json.dumps(connectRequest))
            # Receive connection accepted message
            await rocketChatSocket.recv()

            loginRequest = {
                "msg":
                "method",
                "method":
                "login",
                "id":
                "42",
                "params": [{
                    'resume':
                    'rY9Xg0rN_S6RS0fH-KzdV7m6ptU3GeWlHVZFzwFC2WO'
                }]
            }
            await rocketChatSocket.send(json.dumps(loginRequest))
            # Wait for receiving login user details
            await rocketChatSocket.recv()
            # Wait for method updated signal
            await rocketChatSocket.recv()
            a3 = json.loads(await rocketChatSocket.recv())
            print(a3)
            id = a3['result']['id']
            token = a3['result']['token']

            # step 4
            sub = {
                "msg": "method",
                "method": "createDirectMessage",
                "id": "42",
                "params": ["root"]
            }

            await rocketChatSocket.send(json.dumps(sub))
            # await updated response
            await rocketChatSocket.recv()
            a4 = json.loads(await rocketChatSocket.recv())
            room = a4['result']['rid']

            message = {
                "msg": "method",
                "method": "sendMessage",
                "id": "42",
                "params": [{
                    "rid": room,
                    "msg": "Thanks for contacting NSLHUB\nHow can I help you today..."
                }]
            }

            await rocketChatSocket.send(json.dumps(message))
            await rocketChatSocket.recv()
            await rocketChatSocket.recv()


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Transferring to human chat..")
        asyncio.get_event_loop().run_until_complete(self.hello())
        return []

embed = hub.load(os.getcwd() + "/actions/universal_sentence_encoder")

model = keras.models.load_model(os.getcwd() + '/actions/savedmodel')

def predict_sentiment(sentence):
    sentiment_faces = [ "🤑", "😷", "😡"]
    sent = embed([sentence]).numpy()
    print(type(model))
    pred = model.predict(sent)
    if pred[0] <= 0.4:
        return sentiment_faces[2]
    if pred[0] >= 0.6:
        return sentiment_faces[0]
    return sentiment_faces[1]

class ActionSentimentAnalysis(Action):

    def name(self) -> Text:
        return "action_sentiment_analysis"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent=tracker.latest_message['intent'].get('name')
        if intent[0]=='q':
            num = intent[1:]
            dispatcher.utter_template(template=f"utter_a{num}",emoji=predict_sentiment(tracker.latest_message['text']),tracker=tracker)

        else:
            dispatcher.utter_template(template=f"utter_{intent}",emoji=predict_sentiment(tracker.latest_message['text']),tracker=tracker)
            return []

document_store = FAISSDocumentStore()

converter3 = TextConverter()

processor = PreProcessor(clean_empty_lines=True,
                         clean_whitespace=True,
                         clean_header_footer=True,
                         split_by="sentence",
                         split_length=200,
                         split_respect_sentence_boundary=False)
docs = []
doc_dir = r'actions/wiki/'
for filename in os.listdir(doc_dir):

    if filename.split('.')[-1] == 'txt':
        print("txt file: ", filename)
        d = converter3.convert(os.path.join(doc_dir, filename),
                               meta={"name": filename})
        d = processor.process(d)
        docs.extend(d)

document_store.write_documents(docs)
model_doc = "deepset/roberta-base-squad2"
reader = FARMReader(model_doc, use_gpu=False)
retriever = TfidfRetriever(document_store=document_store)
pipe = ExtractiveQAPipeline(reader, retriever)

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="🙋 I did not understand that.. Searching in the documents")
        dispatcher.utter_message(
            text=pipe.run(query=tracker.latest_message['text'],
                          top_k_retriever=1,
                          top_k_reader=1)["answers"][0]["answer"])

        return []


class ActionMail(Action):
    def name(self) -> Text:
        return "action_mail"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message(text="Started")
        headers = {
            'X-Auth-Token': 'YrSyXcaoUsbphi1FpJk1BmJY9ANWwk5WNqws3yc5M2r',
            'X-User-Id': 'Gd8wWh6bup3rat3ej'
        }
        conversation_id = tracker.sender_id
        #dispatcher.utter_message("The conversation id is {}".format(conversation_id))
        response = requests.get(
            "http://rocketchat:3000/api/v1/channels.messages?roomName=general",
            headers=headers)

        response = json.loads(response.text)
        #msg = response[0]
        User = []
        Bot = []
        index = []
        i = 0
        while "Hey! How can I help you?" not in response["messages"][i]["msg"]:
            if response["messages"][i]["u"]["username"] == "yantr":
                Bot.append(response["messages"][i]["msg"])
                index.append("B")
            else:
                User.append(response["messages"][i]["msg"])
                index.append("U")
            i = i + 1
        Bot.append(response["messages"][i]["msg"])
        index.append("B")
        i = i + 1
        User.append(response["messages"][i]["msg"])
        #index.append("U")
        b = len(Bot) - 1
        u = len(User) - 1
        ind = len(index) - 1
        strz = ("User: " + User[u] + "\n")
        u = u - 1
        while ind >= 0:
            if index[ind] == "U":
                strz = strz + ("User: " + User[u] + "\n")
                u = u - 1
            if index[ind] == "B":
                strz = strz + ("Bot: " + Bot[b] + "\n")
                b = b - 1
            ind = ind - 1

        sender = 'nslsample123@gmail.com'
        receivers = ['noman.siddiqui@nslhub.com', "vinith.reddy@nslhub.com"]
        strz = "The chat is: \n" + strz

        SUBJECT = "Message from rocketchat"

        message = "Test"
        TEXT = strz
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

        message=message.encode('utf8')
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.ehlo

        # Authentication
        s.login("nslsample123@gmail.com", "a1b2c3d4!")

        s.sendmail(sender, receivers, message)
        dispatcher.utter_message(text="Email has been sent")

        return []



class ActionFirstName(Action):
 
    def name(self) -> Text:
        return "action_set_first"
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
           dispatcher.utter_message(text="Recollecting details..")
           return [SlotSet('firstname', None),SlotSet('lastname', None),SlotSet('email', None),SlotSet('phno', None)]


class DetailsForm(FormValidationAction):

    def name(self):
        return "validate_details_form"


    def validate_firstname(
        self, 
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        

        str = value
        x = str.split(" ")
# 1
        if len(x) == 1:
            return {"firstname": value}
        find = 0
        for y in x:
            if(y.isupper()):
                find = find + 1
# 2
        if find == len(x):
            return {"firstname": value}
        
        tex = value
        doc = nlp(tex)
    #    pprint([(X, X.ent_iob_, X.ent_type_, X.tag_) for X in doc])
        tagged_sent = [(w.text, w.tag_) for w in doc]
        normalized_sent = [w.capitalize() if t in ["NN","NNS","NNP","NNPS","JJ","FW","XX","ADD","RB"] else w for (w,t) in tagged_sent]
        normalized_sent[0] = normalized_sent[0].capitalize()
        stri = re.sub(" (?=[\.,'!?:;])", "", ' '.join(normalized_sent))
     #   print(stri)
        #print(doc)
        doc = nlp(stri)
      #  pprint([(X, X.ent_iob_, X.ent_type_, X.tag_) for X in doc]) 
        
        for entity in doc.ents:
            print(entity.text + ' - ' + entity.label_)
# 3
        for entity in doc.ents:
            if entity.label_=="PERSON":
             #   print(entity.text + ' - ' + entity.label_)
                return {"firstname": entity.text}        
            

        for entity in doc.ents:
            str1 = entity.text
            str2 = "Kumar"
            str3 = "Kumar is my name"
            s1 = str1 + ' ' + str2
            s2 = str1 + ' ' + str3
            s3 = str2 + ' ' + str1
            doc1 = nlp(s1)
            doc2 = nlp(s2)
            doc3 = nlp(s3)

            count = 0
            for entity1 in doc1.ents:
              if entity1.label_=="PERSON" and entity1.text!="Kumar":
                  count  = count + 1
                  break
            for entity2 in doc2.ents:
              if entity2.label_=="PERSON" and entity2.text!="Kumar":
                  count = count + 1
                  break
            for entity3 in doc3.ents:
              if entity3.label_=="PERSON" and entity3.text!="Kumar":
                  count = count + 1
                  break
# 4
            if count == 3:
                return {"firstname": entity.text}
# 5,6
        for entity in doc.ents:
            if entity.label_=="ORG":
               # print(entity.text + ' - ' + entity.label_)
                return {"firstname": entity.text}
            if entity.label_=="NORP":
               # print(entity.text + ' - ' + entity.label_)
                return {"firstname": entity.text}
# 7
        for X in doc:
            if X.tag_=="NNP":
                return {"firstname": X.text}        
        
        print("Not present")
        return {"firstname": None}




    def validate_lastname(
        self, 
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        str = value
        x = str.split(" ")
        if len(x) == 1:
            return {"lastname": value}

        find = 0
        for y in x:
            if(y.isupper()):
                find = find + 1
        
        if find == len(x):
            return {"lastname": value}

        tex = value
        doc = nlp(tex)
     #   pprint([(X, X.ent_iob_, X.ent_type_, X.tag_) for X in doc])
        tagged_sent = [(w.text, w.tag_) for w in doc]
        normalized_sent = [w.capitalize() if t in ["NN","NNS","NNP","NNPS","JJ","FW","XX","ADD","RB"] else w for (w,t) in tagged_sent]
        normalized_sent[0] = normalized_sent[0].capitalize()
        stri = re.sub(" (?=[\.,'!?:;])", "", ' '.join(normalized_sent))
        print(stri)
        doc = nlp(stri)
      #  pprint([(X, X.ent_iob_, X.ent_type_, X.tag_) for X in doc])

        for entity in doc.ents:
            if entity.label_=="PERSON":
                print(entity.text + ' - ' + entity.label_)
                return {"lastname": entity.text}        
            
        for entity in doc.ents:
            str1 = entity.text
            str2 = "Kumar"
            str3 = "Kumar is my name"
            s1 = str1 + ' ' + str2
            s2 = str1 + ' ' + str3
            s3 = str2 + ' ' + str1
            doc1 = nlp(s1)
            doc2 = nlp(s2)
            doc3 = nlp(s3)

            count = 0
            for entity1 in doc1.ents:
              if entity1.label_=="PERSON" and entity1.text!="Kumar":
                  count  = count + 1
                  break
            for entity2 in doc2.ents:
              if entity2.label_=="PERSON" and entity2.text!="Kumar":
                  count = count + 1
                  break
            for entity3 in doc3.ents:
              if entity3.label_=="PERSON" and entity3.text!="Kumar":
                  count = count + 1
                  break
            if count == 3:
                return {"lastname": entity.text}

        for entity in doc.ents:
            if entity.label_=="ORG":
                #print(entity.text + ' - ' + entity.label_)
                return {"lastname": entity.text}
            if entity.label_=="NORP":
                #print(entity.text + ' - ' + entity.label_)
                return {"lastname": entity.text}

        for X in doc:
            if X.tag_=="NNP":
                return {"lastname":X.text}

        print("Not present")
        return {"lastname": None}

    
    def validate_email(
        self, 
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        str = value
        x = str.split(" ")
        for y in x:
            print(y)
            if(re.search(regex, y)):
                return {"email": y}
        
        dispatcher.utter_message(text="please enter a valid email")
        return{"email": None}

    def validate_phno(
        self, 
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        regex = '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
        str = value
        x = str.split(" ")
        for y in x:
            print(y)
            if(re.search(regex, y)):
                return {"phno": y}
        
        dispatcher.utter_message(text="please enter a valid phone number")
        return{"phno": None}
