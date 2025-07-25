# download_model.py
import gdown
import os

file_id = '12ruJiBhb3tV30nMSySNpNxQAI9ofGbbS'
url = f'https://drive.google.com/uc?id={file_id}'
output = 'similarity.pkl'

if not os.path.exists(output):
    print("Downloading similarity.pkl from Google Drive...")
    gdown.download(url, output, quiet=False)
else:
    print("similarity.pkl already exists.")