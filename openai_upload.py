from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
vector_store_id=os.environ.get("UFO_DATA_STORE_ID")


def upload_file_to_openai(file_path):
      try:
        with open(file_path, "rb") as file:
            file_content = file.read()
            response = client.beta.vector_stores.files.upload(vector_store_id=vector_store_id, file=(file_path, file_content))
            print(response)
            return response
          
      except Exception as e:
          print(f"Error uploading file to OpenAI: {e}")