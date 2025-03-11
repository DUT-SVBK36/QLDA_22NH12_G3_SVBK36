import tensorflow as tf
import pickle

def load_model_and_encoder(model_path, encoder_path):
    model = tf.keras.models.load_model(model_path)
    with open(encoder_path, "rb") as f:
        label_encoder = pickle.load(f)
    return model, label_encoder