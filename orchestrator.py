from trendy_faiss import TrendyFaiss
from chatbot import Chatbot 
import json

def pipeline(request : dict): 
    metadata = request['metadata']
    messages = request['messages']

    cb = Chatbot()
    llm_parsed_query = cb.get_chatbot_reply(messages)
    reply = llm_parsed_query['response']
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

from flask import Flask, request, jsonify

app = Flask(__name__) 

@app.route('/', methods = ['POST'])
def process_input() : 
    try: 
        data = request.json
        reply = pipeline(data) 
        return {'message', reply}
        
    except Exception as e: 
        return jsonify(
            {'status' : 'error', 
             'message' : str(e)}
        ), 400 

if __name__ == '__main__' : 
    app.run(debug = True)