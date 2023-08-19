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
    combined_dict.update(request['metadata'])

    tf.copy_trendy_photos(k, combined_dict, query_threshhold=query_threshhold, product_threshhold=product_threshhold)

    #to be returned to the user as a message
    return reply 


from flask import Flask, request, jsonify, send_file
from flask_cors import CORS 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods = ['POST'])
def process_input() : 
    try:
        #deleting old images
        import os
        old_images = os.listdir('./matches')
        for image in old_images: 
            os.remove(f'./matches/{image}')
        
        #getting request, making call to fill matches with new img 
        data = request.json
        print(data)
        reply = pipeline(data) 

        #new images 
        images = os.listdir('./matches')
        
        data_obj = {
            'message' : reply, 
            'image_urls' : images 
        }
        
        return data_obj 
        
    except Exception as e: 
        return jsonify(
            {'status' : 'error', 
             'message' : str(e)}
        ), 400 

@app.route('/images/<id>')
def get_image(id : int):
    return send_file('./matches/' + id, mimetype='image/jpeg')


if __name__ == '__main__' : 
    app.run(debug = True)