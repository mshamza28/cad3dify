import sys
import os
# Add the project root directory to Python's path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
 
import argparse
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
 
load_dotenv()
from cad3dify import generate_step_from_2d_cad_image
 
 
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_type", type=str, default="gpt")
    return parser.parse_args()
 
 
args = parse_args()
 
st.title("2D Drawing to 3D CAD Converter")
 
uploaded_file = st.sidebar.file_uploader("Select an image file", type=["jpg", "jpeg", "png"])
 
# Display the image when uploaded
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    ext = os.path.splitext(uploaded_file.name)[1]
    st.image(image, caption="Uploaded Image", use_container_width=True)
    st.write("Image Size: ", image.size)
    with open(f"temp{ext}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    with st.spinner("Processing image..."):
        try:
            generate_step_from_2d_cad_image(
                f"temp{ext}", "output.step", model_type=args.model_type
            )
            st.success("3D CAD data generation complete!")
            
            # Add a download button for the generated STEP file
            if os.path.exists("output.step"):
                with open("output.step", "rb") as f:
                    st.download_button(
                        label="Download STEP file",
                        data=f,
                        file_name="output.step",
                        mime="application/step"
                    )
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")
            st.exception(e)  # This will display the full traceback
else:
    st.write("No image has been uploaded.")
