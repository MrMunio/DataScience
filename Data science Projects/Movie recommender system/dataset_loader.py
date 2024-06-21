# run the following code to download the dataset if not already downloaded

import os
import requests
os.chdir("..") # Navigate to parent directory

# Define the URL and the target directory
url = "https://files.grouplens.org/datasets/movielens/ml-25m.zip"
directory = "dataset"
filename = os.path.join(directory, "ml-25m.zip")

# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Download the file
response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(f"File downloaded and saved as {filename}")
else:
    print("Failed to download the file")


# Extract the zip file and ready the datasets

import zipfile
import shutil
zip_filename = os.path.join(directory, "ml-25m.zip")

with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
    for file in ['ml-25m/movies.csv', 'ml-25m/ratings.csv']:
        # Extract the file to the directory, maintaining the directory structure
        zip_ref.extract(file, directory)
        # Move the extracted file to the main dataset directory and remove the subdirectory
        extracted_path = os.path.join(directory, file)
        final_path = os.path.join(directory, os.path.basename(file))
        shutil.move(extracted_path, final_path)  # Use shutil.move to overwrite existing files
    print(f"Extracted movies.csv and ratings.csv to {directory}")

# Delete the zip file
# os.remove(zip_filename)
# print(f"Deleted the zip file: {zip_filename}")

# Delete the ml-25m subdirectory
shutil.rmtree(os.path.join(directory, 'ml-25m'))
print(f"Deleted the subdirectory: {os.path.join(directory, 'ml-25m')}")

print("data dependency for main.py is satisfied...")