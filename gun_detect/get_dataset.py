import requests
import zipfile
import os


# Download the file
#url = "https://universe.roboflow.com/ds/L76hzT4so5?key=tpRs7o81ki"
url = "https://app.roboflow.com/ds/j1BEJld3NB?key=2PardK2OTb"
response = requests.get(url, stream=True)
with open("roboflow.zip", "wb") as file:
    for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)

# Unzip the file
with zipfile.ZipFile("roboflow.zip", 'r') as zip_ref:
    zip_ref.extractall()

# Remove the zip file
os.remove("roboflow.zip")