from typing import List
from transformers import AutoTokenizer, AutoModel 
import torch 
from sklearn.preprocessing import normalize
import faiss


class FaissDB(): 
    def __init__(self):
        #making embedding models
        model_name = "bert-base-uncased" 
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name) 
        self.embedding_dim = 768
        self.index = faiss.IndexFlatL2(self.embedding_dim)

    #func to be called on each product string
    def get_text_embedding(self, input_text: str): 
        inputs = self.tokenizer(input_text, return_tensors='pt', padding = True, truncation = True) 
        with torch.no_grad(): 
            outputs = self.model(**inputs) 
            embeddings = outputs.last_hidden_state.mean(dim = 1) 
            
        text_embedding = embeddings.numpy() 
        normalized_embedding = normalize(text_embedding, norm = 'l2', axis = 1)
        print('Text embedding created')
        return normalized_embedding

    def populate_faiss(self, file_path:str = "./embeddings.txt"): 
        #getting each prod string to make embedding
        with open(file_path, 'r') as file: 
            content = file.read() 

        #creating faiss instance

        #for each product get embedding and push into index
        products = content.strip().split('\n\n') 
        for product in products[:1000]: #TODO change to all 
            text_embedding = self.get_text_embedding(product) 
            self.index.add(text_embedding) 

        #write to disk
        faiss.write_index(self.index, "product_embeddings.index")
        print("Faiss index created")
    
    def _load_faiss_index(self, index_path : str): 
        index = faiss.read_index(index_path)               
        return index
    
    def get_k_similar(self, k : int, text : str) -> List[str]:
        text_embedding = self.get_text_embedding(text) 
        text_embedding = normalize(text_embedding, norm = 'l2', axis=1)
        index = self._load_faiss_index("./product_embeddings.index")    
        _, indices = index.search(text_embedding, k)
        
        with open('./embeddings.txt', 'r') as file: 
            content = file.read() 
            
        products = content.strip().split('\n\n')
        closest_prods = []
        for idx in indices[0]: 
            nearest_prod_desc = products[idx]
            closest_prods.append(nearest_prod_desc) 
        return closest_prods
    
fdb = FaissDB()
# fdb.populate_faiss()

prod_desc = fdb.get_k_similar(k = 3, text = """
id : 19094
gender : Women
masterCategory : Footwear
subCategory : Footwear
articleType : Shoes
baseColour : Blue
season : Summer
year : 2011.0
usage : Ethnic
productDisplayName :            
""")

for prod in prod_desc : 
    id = prod.split('\n')[0].split(' : ')[-1]
    import shutil

    source_path = f'./images/{id}.jpg'
    destination_path = f'./matches/{id}.jpg'

    # Copy the file
    shutil.copy(source_path, destination_path)


