import os
import requests
import zipfile
from pathlib import Path
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / '.env')

DATA_DIR = (REPO_ROOT / os.getenv("DATA_DIR")).resolve()

url = "https://www.ipb.uni-bonn.de/html/projects/Pheno4D/Pheno4D.zip"

response = requests.get(url, stream=True)

print(
    """
    [Notice]
    This is a 5 gigabyte zip file. Expect the download to take some time.
    """
)

with open(DATA_DIR / "data.zip", "wb") as file:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            file.write(chunk)

with zipfile.ZipFile(DATA_DIR / 'data.zip', 'r') as zip_file:
    zip_file.extractall(DATA_DIR)

os.remove(DATA_DIR / "data.zip")

for item in (DATA_DIR / "Pheno4D").iterdir():
    new_loc = DATA_DIR / item.name
    os.rename(item, new_loc)

os.rmdir(DATA_DIR / "Pheno4D")

