from trendy_faiss import TrendyFaiss
from chatbot import Chatbot 
import json

def pipeline(request): 
    metadata = request['metadata']
    messages = request['messages']

    metadata_string = json.dumps(metadata)

    cb = Chatbot()
    llm_parsed_query = json.dumps(cb.get_chatbot_reply(messages))
    llm_parsed_query = llm_parsed_query.replace('"', '')
    llm_parsed_query = llm_parsed_query.replace(',', '\n')
    llm_parsed_query = llm_parsed_query[1:]
    llm_parsed_query = llm_parsed_query[:len(llm_parsed_query) - 1] 
    print(llm_parsed_query)
    
    k = metadata['k']
    query_threshhold = metadata['similarity']
    product_threshhold = 1 - metadata['similarity']

    tf = TrendyFaiss() 
    tf.populate_faiss(llm_parsed_usr_query=llm_parsed_query)
    tf.copy_trendy_photos(k, llm_parsed_query + metadata_string, query_threshhold=query_threshhold, product_threshhold=query_threshhold)


req = {
    'metadata' : {
        'k' : 5, 
        'similarity' : 0.7
    }, 
    'messages' : [
        {
            'role' : 'user', 
            'content' : 'Men footwear. Black shoes. Puma'
        }
    ]
}

pipeline(req)