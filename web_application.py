import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import streamlit as st

labels = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

model = tf.keras.models.load_model("EcoIdentify_savedmodel")

def preprocess_image(file):
    img = Image.open(file).convert("RGB")
    img = img.resize((256, 256))
    img = np.array(img).astype("float32")
    img = img / 127.5 - 1.0  
    img = np.expand_dims(img, axis=0)
    return img, Image.open(file)

st.set_page_config(
    page_title="EcoIdentify by EcoClim Solutions",
    page_icon="https://ecoclimsolutions.files.wordpress.com/2024/01/rmcai-removebg.png?resize=48%2C48",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.image("https://ecoclimsolutions.files.wordpress.com/2024/01/rmcai-removebg.png?resize=48%2C48")
st.title("EcoIdentify by EcoClim Solutions")
st.header("Upload a waste image to find its category")

st.markdown("*Our dataset performs best on images with a white background.*")

opt = st.selectbox("How do you want to upload the image?", ("Please Select", "Upload image from device"))

image_display = None
image_array = None

if opt == "Upload image from device":
    file = st.file_uploader("Select", type=["jpg", "png", "jpeg"])
    if file:
        image_array, image_display = preprocess_image(file)

if image_display is not None:
    st.image(image_display, width=256, caption="Uploaded Image")

    if st.button("Predict"):
        infer = model.signatures["serving_default"]
        output = infer(tf.constant(image_array))
        prediction = output[list(output.keys())[0]].numpy()[0]
        predicted_index = np.argmax(prediction)
        predicted_class = labels[predicted_index]
        confidence = prediction[predicted_index]
        st.success(f"Prediction: {predicted_class.upper()} (Confidence: {confidence:.2f})")
        st.subheader("Class probabilities")
        for label, prob in zip(labels, prediction):
            st.write(f"{label}: {prob:.2f}")
