import os
from deepface import DeepFace
import streamlit as st
from PIL import Image
from datetime import datetime

# Directories for known faces and temp images
face_dir = "faces/"
temp_dir = "temp_images/"

# Create temp directory if not exists
os.makedirs(temp_dir, exist_ok=True)

# Function to load known faces and names
def load_known_faces(face_dir):
    if not os.path.exists(face_dir) or not os.listdir(face_dir):
        return [], []
    return face_dir, [subdir for subdir in os.listdir(face_dir) if os.path.isdir(os.path.join(face_dir, subdir))]

# Function to recognize a face
def recognize_face(face_dir, image_path):
    try:
        result = DeepFace.find(img_path=image_path, db_path=face_dir, model_name="VGG-Face", enforce_detection=False)
        if len(result) > 0:
            df = result[0]
            if not df.empty:
                match = df.iloc[0]
                matched_name = os.path.basename(os.path.dirname(match['identity']))
                return matched_name
        return "Unknown"
    except Exception as e:
        return f"Error: {e}"

# Hardcoded Secret Santa Assignments
santa_pairs = {
    "PETROS": "ANDREW",
    "ANDREW": "SOTIRIS",
    "SOTIRIS": "MARIA",
    "MARIA": "ELENI",
    "ELENI": "KALLIOPI",
    "KALLIOPI": "GIORGOS",
    "GIORGOS": "ALEX",
    "ALEX": "MAXI",
    "MAXI": "MANOLIS",
    "MANOLIS": "PETROS"
}

# Initialize the Streamlit app
st.title("2024 Secret Santa 🎅")
st.text("Take your picture to discover your Secret Santa assignment!")

# Load known faces
face_dir, known_names = load_known_faces(face_dir)

# File uploader for photo submission
uploaded_file = st.file_uploader("Upload a photo (JPG or PNG)", type=["jpg", "png"])

# Check if a name has been recognized
if uploaded_file:
    # Save the uploaded image with a timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_image_path = os.path.join(temp_dir, f"temp_{timestamp}.jpg")
    with open(temp_image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display loading spinner while recognizing the face
    with st.spinner("Processing..."):
        # Recognize the face in the image
        name = recognize_face(face_dir, temp_image_path)

    # Show recognized name immediately
    if name != "Unknown" and name in santa_pairs:
        st.subheader(f"Hello, {name.upper()}!")

        # Now handle the "Show who to get gift for!!" button
        if st.button("Show me who to get gift for!"):
            with st.spinner("Fetching your Secret Santa..."):
                # Get recipient's name
                recipient = santa_pairs[name].upper()

                # Get recipient's image
                recipient_dir = os.path.join(face_dir, recipient)
                recipient_image = None
                if os.path.exists(recipient_dir):
                    recipient_images = [file for file in os.listdir(recipient_dir) if file.endswith((".jpg", ".png"))]
                    if recipient_images:
                        recipient_image = os.path.join(recipient_dir, recipient_images[0])

                # Display recipient's name and image
                st.subheader(f"Your Secret Santa is: {recipient}!")
                if recipient_image:
                    st.image(recipient_image, caption=f"{recipient}'s Picture", use_column_width=True)

    else:
        st.subheader("Face not recognized. Please try again.")

