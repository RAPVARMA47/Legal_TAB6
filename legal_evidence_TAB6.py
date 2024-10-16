import base64
from PIL import Image
import io
import streamlit as st
import requests
 

api_key = st.secrets["OPENAI_API_KEY"]
 
# Function to encode the image
def encode_image(image_path):
    image = Image.open(image_path)
    buffered = io.BytesIO()
    image_format = image.format if image.format else 'PNG'  # Default to PNG if format is None
    image.save(buffered, format=image_format)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def main():
 
        image_path = st.file_uploader("Upload your evidence here:", type=["png", "jpg", "jpeg"])
        if image_path:
            with st.expander("Uploaded Evidence"):
                st.image(image_path)
            query = st.text_input("Enter your query here:")
            if query.lower():
                with st.spinner("Analyzing the Evidence"):
                    prompt_template = "You are an legal assistance bot who is an expert in Analyzing the evidences and provide the complete insight about the evidence provided even without missing any minute detail"
           
                    # Getting the base64 string
                    base64_image = encode_image(image_path)
                   
                    headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                    }
                   
                    payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {
                        "role": "user",
                        "content": [
                            {
                            "type": "text",
                            "text": prompt_template
                            },
                            {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                            }
                        ]
                        }
                    ],
                    "max_tokens": 4096
                    }
                   
                    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
           
                    st.write(response.json()['choices'][0]['message']['content'])
                    
                    
                    
if __name__ == "__main__":
    main()