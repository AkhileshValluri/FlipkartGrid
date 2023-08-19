from transformers import AutoTokenizer, AutoModel
import torch 
from sklearn.preprocessing import normalize
import faiss
from populate_faiss import ImageFaiss, copy_images_to_matches

class TrendyFaiss() : 
    def __init__(self): 
        #making embedding models 
        model_name = "distilbert-base-uncased"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name) 
        self.embedding_dim = 768
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        
        self.faissdb = ImageFaiss()

        self.weights = {
            'gender' : 1, 
            'articleType' : 4, 
            'baseColour' : 1
        }

    def _get_text_preprocessing(self, response : dict, weights : dict) :
        """
        Preprocessing text to extract information from desc
        Kwargs define weights for different categories"""
        input_string = "" 
        print(response)
        for key in response.keys(): 
            weight = weights[key] if key in weights.keys() else 1
            for _ in range(weight): 
                    if isinstance(response[key], list): 
                        for val in response[key]:
                            input_string += val + ' '
                    else:
                        input_string += str(response[key]) + ' '
        print(input_string)
        return input_string
                    
            

    def get_text_embedding(self, \
        input_text : str, \
        weights : dict = {
            'gender' : 0, 
            'articleType' : 3, 
            'baseColour' : 1
        }) : 

        
        input_text = self._get_text_preprocessing(input_text, weights) 
        
        inputs = self.tokenizer(input_text, return_tensors = 'pt', padding = True, truncation = True)
        with torch.no_grad(): 
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim = 1) 
        
        text_embedding = embeddings.numpy() 
        normalized_embedding = normalize(text_embedding, norm = 'l2', axis = 1)
        return normalized_embedding 

    def populate_faiss(self, llm_parsed_usr_query : dict): 
        """Populates trendy query faiss
        llm_parsed_usr_query : object with articleType, baseColour, gender info"""
        with open('./trendy_faiss.txt', 'a') as file: 
            file.write(self._get_text_preprocessing(llm_parsed_usr_query, self.weights)) 
            file.write('\n')
            print(self._get_text_preprocessing(llm_parsed_usr_query, self.weights))
        
        text_embedding = self.get_text_embedding(llm_parsed_usr_query)
        self.index.add(text_embedding)
        faiss.write_index(self.index, "trendy_faiss.index")

    def _load_faiss_index(self): 
        index = faiss.read_index('./trendy_faiss.index')
        return index 

    def get_k_similar(self, k : int, text : dict, threshhold : float = 0.8):
        """k -> number of similar to consider 
        text -> query for which to find similar 
        threshhold -> cosine similarity threshhold"""
        text_embedding = self.get_text_embedding(text) 
        text_embedding = normalize(text_embedding, norm = 'l2', axis = 1) 
        index = self._load_faiss_index()
        distances, indices = index.search(text_embedding, k) 

        with open('./trendy_faiss.txt' , 'r') as file: 
            content = file.read() 
        
        products = content.strip().split('\n\n')
        closest_qrys = [] 
        for dist, idx in zip(distances[0], indices[0]): 
            nearest_qrys = products[idx]
            cosine_similarity = 1 / (1 + dist) 
            print(cosine_similarity)
            if cosine_similarity >= threshhold: 
                closest_qrys.append(nearest_qrys)
                
        closest_qrys = [text] + closest_qrys
        return closest_qrys
    
    def copy_trendy_photos(self, k : int, text : str, query_threshhold : float = 0.9, product_threshhold : float = 0.2): 
        """for all similar trendy queries, get k similar products for each"""
        trendy_queries = self.get_k_similar(k = k, text = text, threshhold = query_threshhold)

        for query in trendy_queries: 
            copy_images_to_matches(prod_desc = self.faissdb.get_k_similar(k, query, product_threshhold))
    