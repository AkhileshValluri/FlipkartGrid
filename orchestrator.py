from trendy_faiss import TrendyFaiss
from chatbot import Chatbot 
import json

def pipeline(request : dict): 
    metadata = request['metadata']
    messages = request['messages']

    cb = Chatbot()
    # llm_parsed_query = cb.get_chatbot_reply(messages)
    llm_parsed_query = {'gender': 'Men', 'articleType': ['Casual Shoes', 'Formal Shoes', 'Sports Sandals'], 'baseColour': 'Black'}
    print(llm_parsed_query)
    
    k = metadata['k']
    query_threshhold = metadata['similarity']
    product_threshhold = 1 - metadata['similarity']

    tf = TrendyFaiss() 
    tf.populate_faiss(llm_parsed_usr_query=llm_parsed_query)
    
    combined_dict = llm_parsed_query
    combined_dict.update(req['metadata'])

    tf.copy_trendy_photos(k, combined_dict, query_threshhold=query_threshhold, product_threshhold=query_threshhold)


req = {
    'metadata' : {
        'k' : 5, 
        'similarity' : 0.7, 
        'location' : 'hyderabad', 
        'age' : 100
    }, 
    'messages' : [
        {
            'role' : 'user', 
            'content' : 'Men footwear. Black shoes. Puma'
        }
    ]
}

pipeline(req)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class RequestPayload(BaseModel):
    metadata: dict
    messages: List[Message]

class ResponsePayload(BaseModel):
    result: str

@app.post("/process")
def process_request(payload: RequestPayload):
    try:
        metadata = payload.metadata
        messages = payload.messages

        # Your processing logic here

        result = "Processed successfully"
        
        response_payload = ResponsePayload(result=result)
        return response_payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
