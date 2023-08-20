from trendy_faiss import TrendyFaiss
from chatbot import Chatbot 
import json

def pipeline(request : dict) ->str: 
    """
    Puts entire query through a pipeline and populates matches with relevent images
    request should have metadata and messages
    """

    metadata = request['metadata']
    messages = request['messages']

    cb = Chatbot()
    llm_parsed_query = cb.get_chatbot_reply(messages, metadata)
    reply = llm_parsed_query['response']
    print(llm_parsed_query)
        
    k = metadata['k']
    query_threshhold = metadata['similarity']
    product_threshhold = 1 - metadata['similarity']

    tf = TrendyFaiss() 
    tf_populate_dict = llm_parsed_query
    tf_populate_dict.update(metadata)
    tf.populate_faiss(llm_parsed_usr_query=tf_populate_dict)
    
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
        import os        
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

@app.route('/', methods = ['GET'])
def new_user(): 
    #deleting old images
    import os
    old_images = os.listdir('./matches')
    for image in old_images: 
        os.remove(f'./matches/{image}')
    print('all files cleared')
    return {'message' : 'All files cleared'}

if __name__ == '__main__' : 
    app.run(debug = True)