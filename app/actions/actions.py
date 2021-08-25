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
from rasa_sdk.events import ActionReverted
import en_core_web_md
nlp = en_core_web_md.load()
from rasa_sdk.events import ActionReverted, SlotSet, FollowupAction, UserUtteranceReverted
import requests
import os
import asyncio

import websockets
#from rocketchat.api import RocketChatAPI
#from requests.auth import HTTPBasicAuth 


class ActionSessionId(Action):
    def name(self) -> Text:
        return "action_session_id"

    async def run(
    self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        conversation_id=tracker.sender_id
        dispatcher.utter_message("The conversation id is {}".format(conversation_id))
        return []

class ActionCreateUser(Action):
     def name(self) -> Text:
         return "action_create_user"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         #AllUsers()
         Body = {'client_id': 'ptest', 'username': 'ptesttenantadmin', 'password': 'test', 'grant_type': 'password'}
    
         #headers = {'Accept': 'application/json, text/plain, */*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36', 'Content-Type' :'application/x-www-form-urlencoded', 'Accept-Language': 'en'}
    
         response = requests.post("https://iam.nslhub.com/auth/realms/ptest/protocol/openid-connect/token",data = Body)
         print(response.status_code)
         auth_response_json = response.json()
         auth_token = auth_response_json["access_token"]
         auth_token_header_value = "bearer %s" % auth_token

         headers1 = {'authority' : 'ptest.qa3.nslhub.com', 'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"', 'traceparent': '00-2b29240176c0f89ead3e743c85736650-774d330740f0dddf-01', 'accept-language': 'en', 'sec-ch-ua-mobile': '?0', 'authorization':auth_token_header_value, 'content-type':'application/json', 'accept':'application/json, text/plain, */*', 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36', 'origin':'https://ptest.qa3.nslhub.com', 'sec-fetch-site':'same-origin', 'sec-fetch-mode':'cors', 'sec-fetch-dest':'empty', 'referer':'https://ptest.qa3.nslhub.com/admin/adduser','cookie':'_ga=GA1.1.738583816.1615352728; _ga_GSGN4DSWQV=GS1.1.1615352728.1.1.1615352744.0'}
         Body1 = json.dumps({
            "isEnabled": True,
            "name": tracker.get_slot("firstname"),
            "password": "test",
            "firstName": tracker.get_slot("firstname"),
            "lastName": tracker.get_slot("lastname"),
            "email": tracker.get_slot("email"),
            "environments": [
            "development"
            ]
         })
         response1 = requests.post("https://ptest.qa3.nslhub.com/dsd-orch/cdm/api/cdm/create/user", headers=headers1, data = Body1)
         print(response1.status_code)
         print(response1.text)
         return []



class ActionCreateDirectMessage(Action):
#
    def name(self) -> Text:
        return "action_create_direct_message"

    # async def hello(self,tracker):
    #     uri = "ws://rocket:3000/websocket"
    #     async with websockets.connect(uri) as rocketChatSocket:
    #         # Receive ack
    #         await rocketChatSocket.recv()

    #         connectRequest = {
    #             "msg": "connect",
    #             "version": "1",
    #             "support": ["1", "pre2", "pre1"]
    #         }
    #         await rocketChatSocket.send(json.dumps(connectRequest))
    #         # Receive connection accepted message
    #         await rocketChatSocket.recv()
    #         loginRequest = {
    #             "msg":
    #             "method",
    #             "method":
    #             "login",
    #             "id":
    #             "42",
    #             "params": [{
    #                 'resume':
    #                 'YV_lTAi9vRkB6bJe_XDxRh66LqagdI0MldCYQLQPH4R'
    #             }]
    #         }
    #         await rocketChatSocket.send(json.dumps(loginRequest))
    #         # Wait for receiving login user details
    #         await rocketChatSocket.recv()
    #         # Wait for method updated signal
    #         await rocketChatSocket.recv()
    #         a3 = json.loads(await rocketChatSocket.recv())
    #         print(a3)
    #         id = a3['result']['id']
    #         token = a3['result']['token']

    #         # step 4
    #         sub = {
    #             "msg": "method",
    #             "method": "createDirectMessage",
    #             "id": "42",
    #             "params": ["customer"]
    #         }

    #         await rocketChatSocket.send(json.dumps(sub))
    #         # await updated response
    #         await rocketChatSocket.recv()
    #         a4 = json.loads(await rocketChatSocket.recv())
    #         room = a4['result']['rid']

    #         #Sending chat history
    #         hist = tracker.events
    #         chat = []

    #         for i in hist[::-1]:
    #             if i['event']=="bot":
    #                 str="YANTR : "+i["text"]+"\n"
    #                 chat.append(str)
    #             elif i['event']=="user":
    #                 str="USER : "+i["text"]+"\n"
    #                 chat.append(str)
    #                 if i["parse_data"]["intent"]["name"]== "greet":
    #                     break
    #         chatr=chat[::-1]
            
    #         strz = "Thanks for contacting NSLHUB\n This is user's chat history with the bot : \n\n"
    #         strz=strz+"-------------------------------------------------------------------------------------------------\n\n"
    #         for x in chatr:
    #             strz=strz+x
    #             strz=strz+"\n"
    #         strz= strz+ "\n####################################\n"
    #         strz= strz+ "####################################\n"
    #         strz= strz +"####################################\n\n\nMoving ahead,How can I help you today...\n"
    #         message = {
    #             "msg": "method",
    #             "method": "sendMessage",
    #             "id": "42",
    #             "params": [{
    #                 "rid": room,
    #                 "msg": strz
    #             }]
    #         }

    #         await rocketChatSocket.send(json.dumps(message))
    #         await rocketChatSocket.recv()
    #         await rocketChatSocket.recv()

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            #asyncio.get_event_loop().run_until_complete(self.hello(tracker))
            headers = {'Content-type': 'application/json'}
            sid=tracker.sender_id
            data = json.dumps({"action": "handover","sessionId": sid,"actionData": {"targetDepartment": "Livechat1" }})
            response = requests.post('http://192.168.49.2:32211/api/apps/public/646b8e7d-f1e1-419e-9478-10d0f5bc74d9/incoming', headers=headers, data=data)
            
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

# #converter2 = PDFToTextConverter()
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

    # if filename.split('.')[-1] == 'pdf':
    #     print("Pdf file: ",filename)
 
    #     d = converter2.convert(os.path.join(doc_dir,filename), meta={"name": filename})
    #     d = processor.process(d)
    #     docs.extend(d)

document_store.write_documents(docs)
model_doc = "deepset/roberta-base-squad2"
reader = FARMReader(model_doc, use_gpu=False)
retriever = TfidfRetriever(document_store=document_store)
pipe = ExtractiveQAPipeline(reader, retriever)

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def wait(self,dispatcher):
        dispatcher.utter_message(text="🙋 I did not find anything in FAQs... Searching the knowledge base")
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        self.wait(dispatcher)
        try:
            search = pipe.run(query=tracker.latest_message['text'], top_k_retriever=1, top_k_reader=1)
        except Exception as e:
            search = {'query': tracker.latest_message['text'],'answers': [{'answer': None,'score': 0,'probability': 0,'context': None,'offset_start': 0,'offset_end': 0,'document_id': None, 'meta': {}}]}

        text=search["answers"][0]["answer"]
        confidence=search["answers"][0]["probability"]
        if text != "None" and confidence>0.01:
            dispatcher.utter_message(text)
        else:
            dispatcher.utter_message(text="🙋 I did not find anything in Knowledge base... Shall I transfer it to human agent?")   
        return []


class Actionsearch(Action):
    def name(self) -> Text:
        return "action_search"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        return [ActionReverted()]


class ActionMail(Action):
    def name(self) -> Text:
        return "action_mail"
      
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Sending mail...Please wait\n")
        hist = tracker.events
        chat = []

        for i in hist[::-1]:
            if i['event']=="bot":
                str="YANTR: "+i["text"]+"\n"
                chat.append(str)
            elif i['event']=="user":
              str="USER: "+i["text"]+"\n"
              chat.append(str)
              if i["parse_data"]["intent"]["name"]== "greet":
                  break
        chatr=chat[::-1]
        strz = "The chat is: \n"
        for x in chatr:
            strz=strz+x
        
        sender = 'nslsample123@gmail.com'
        receivers = ['noman.siddiqui@nslhub.com', "vinith.reddy@nslhub.com"]

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
            for event in tracker.events:
                if event.get("event") == "bot":
                    str = event.get("text")
            if "Please once check your details:" not in str:
                return[FollowupAction(name="action_default_fallback")]
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
