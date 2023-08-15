import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.layers import Input, Embedding, Flatten, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy

# Load and preprocess the data
data_path = "your_data_file.txt"  # Replace with the actual path to your data file
with open(data_path, 'r') as file:
    lines = file.readlines()

# Extract features and labels
features = []
labels = []
current_feature = {}
for line in lines:
    if line.strip() == "":
        features.append(current_feature)
        current_feature = {}
    else:
        key, value = line.strip().split(" : ")
        current_feature[key] = value
labels.append(current_feature)

# Convert data to NumPy arrays
features = np.array(features)
labels = np.array(labels)

# Encode categorical features
label_encoders = {}
for feature in features.T:
    label_encoder = LabelEncoder()
    encoded_feature = label_encoder.fit_transform(feature)
    label_encoders[feature[0]] = label_encoder
    features[:, feature[0]] = encoded_feature

# Define embedding sizes
embedding_dims = {
    'gender': 8,
    'masterCategory': 16,
    'subCategory': 16,
    'articleType': 16,
    'baseColour': 16,
    'season': 8,
    'usage': 16,
    'productDisplayName': 32,
}

# Create the embedding model
input_layers = []
embedding_layers = []
for feature in embedding_dims.keys():
    input_layer = Input(shape=(1,))
    embedding_layer = Embedding(len(label_encoders[feature].classes_), embedding_dims[feature])(input_layer)
    input_layers.append(input_layer)
    embedding_layers.append(embedding_layer)
embedding = Flatten()(embedding_layers)
output_layer = Dense(len(label_encoders['articleType'].classes_), activation='softmax')(embedding)

model = Model(inputs=input_layers, outputs=output_layer)
model.compile(optimizer=Adam(), loss=SparseCategoricalCrossentropy(), metrics=[SparseCategoricalAccuracy()])

# Train the model
x = [features[:, i] for i in range(features.shape[1])]
y = labels[:, 'articleType']
model.fit(x, y, batch_size=32, epochs=10)

# Save the trained model
model.save("embedding_model.h5")
