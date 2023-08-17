import os
import numpy as np
import cv2
import faiss
import tensorflow as tf
import shutil 

class ImageEmbedding:
    def __init__(self, embedding_dim=128, index_filename="image_faiss.index", target_resolution=(96, 96)):
        self.embedding_dim = embedding_dim
        self.index_filename = index_filename
        self.target_resolution = target_resolution
        self.index = None
        self.image_paths = []

    def load_images(self, image_folder="./images"):
        self.image_paths = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder)]
        embeddings = []

        # Load images and create embeddings
        for image_path in self.image_paths:
            image = cv2.imread(image_path)
            image = self.resize_image(image)  # Resize to the target resolution
            embedding = self.compute_embedding(image)
            embeddings.append(embedding)

        self.index = faiss.IndexFlatL2(self.embedding_dim)
        embeddings = np.array(embeddings, dtype=np.float32)
        self.index.add(embeddings)

        faiss.write_index(self.index, self.index_filename)

    def resize_image(self, image):
        return cv2.resize(image, self.target_resolution)

    def compute_embedding(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image / 255.0  # Normalize image pixels to [0, 1]

        # Load a pre-trained model (e.g., MobileNetV2)
        model = tf.keras.applications.MobileNetV2(weights="imagenet", include_top=False)
        features = model.predict(np.expand_dims(image, axis=0))
        embedding = features.flatten()  # Flatten the feature tensor

        return embedding

    def query_k_similar(self, query_embedding, k=5):
        if self.index is None:
            self.load_index()

        _, ids = self.index.search(query_embedding.reshape(1, -1), k)
        
        similar_image_paths = [self.image_paths[id] for id in ids[0]]
        
        # Create the "matches" directory if it doesn't exist
        matches_dir = os.path.join(os.path.dirname(self.index_filename), "matches")
        os.makedirs(matches_dir, exist_ok=True)
        
        # Copy similar images to the "matches" directory
        for image_path in similar_image_paths:
            image = cv2.imread(image_path)
            image = self.resize_image(image)  # Resize to the target resolution
            shutil.copy(image_path, matches_dir)
            print(f"Copied {image_path} to {matches_dir}")
        
        return similar_image_paths

    def load_index(self):
        self.index = faiss.read_index(self.index_filename)

ie = ImageEmbedding() 
ie.load_images()