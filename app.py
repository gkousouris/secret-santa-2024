import os
from deepface import DeepFace
import streamlit as st
from PIL import Image

# Directory containing known face images
face_dir = "faces/"

# Function to load known faces and names
def load_known_faces(face_dir):
    if not os.path.exists(face_dir) or not os.listdir(face_dir):
        st.error("Face directory is empty or does not exist.")
        return [], []
    return face_dir, [os.path.splitext(file)[0] for file in os.listdir(face_dir) if file.endswith(('.jpg', '.png'))]

# Function to recognize a face
def recognize_face(face_dir, image_path):
    try:
        result = DeepFace.find(img_path=image_path, db_path=face_dir, model_name="VGG-Face")
        if len(result) > 0:
            df = result[0]
            if not df.empty:
                match = df.iloc[0]
                matched_name = os.path.splitext(os.path.basename(match['identity']))[0]
                return matched_name
        return "Unknown"
    except Exception as e:
        return f"Error: {e}"

# Initialize the Streamlit app
st.title("2024 Secret Santa")
st.text("Take your picture to receive who you have!")

# Load known faces
face_dir, known_names = load_known_faces(face_dir)
if not known_names:
    st.warning("Please add images to the 'faces/' directory to proceed.")

# File uploader for photo submission
uploaded_file = st.file_uploader("Upload a photo (JPG or PNG)", type=["jpg", "png"])

if uploaded_file:
    # Save the uploaded image temporarily
    temp_image_path = "temp_frame.jpg"
    with open(temp_image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Display the uploaded image
    st.image(temp_image_path, caption="Uploaded Image", use_column_width=True)

    # Recognize the face in the image
    name = recognize_face(face_dir, temp_image_path)
    st.subheader(f"Hello, {name}!")

