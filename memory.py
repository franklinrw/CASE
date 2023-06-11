import os
import csv
from huggingface_hub import Repository
from huggingface_hub import hf_hub_download

DATASET_REPO_URL = "https://huggingface.co/datasets/FranklinWillemen/demo_storage"
DATA_FILENAME = "test.csv"
DATA_FILE = os.path.join("data", DATA_FILENAME)
HF_TOKEN = os.environ.get("HF_TOKEN")

repo = Repository(
    local_dir="data", clone_from=DATASET_REPO_URL, use_auth_token=HF_TOKEN
)

def save_context(context):
    with open("test", "a") as csvfile:
        for message in context:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "message"])
            writer.writerow(
                {"name": message['role'], "message": message['content']}
            )
        commit_url = repo.push_to_hub()
        print(commit_url)

def load_context():
    file_path = hf_hub_download(DATASET_REPO_URL, filename="test.csv")
    file = open(file_path, "r")
    reader = csv.DictReader(file)
    myList = list()
    for dictionary in reader:
        myList.append(dictionary)
    return file_path