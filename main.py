# Load Packages
import google.generativeai as genai
from PIL import Image
import os
import streamlit as st
# Load environment variables
from dotenv import load_dotenv
load_dotenv()


# Load API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Load the model
model = genai.GenerativeModel('gemini-pro-vision')

# Set page theme name
st.set_page_config(page_title="Multi Language Invoice Extractor")
st.header("Gemini Application")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Take image from user and transform it into image parts
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")




# function to generate results based on the input parameters
def get_gemini_response(input, image, prompt):
    response = model.generate_content(
        [input, image[0], prompt])
    return response.text


image = ""
INPUT = ""
# Function to get the image from user
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    input = st.text_input("Input Prompt: ", key="input")
    INPUT = input

submit = st.button("Tell me about the image")
input_prompt = """
You are an expert in understanding invoices. We will upload an image as invoice, you will have to answer any question based on the uloaded invoice image
"""

if submit:
    image_data = input_image_setup(uploaded_file=uploaded_file)
    response = get_gemini_response(input_prompt,image_data,INPUT)
    st.subheader("The response is")
    st.write(response)