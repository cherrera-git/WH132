from google.cloud import storage
from google.oauth2 import service_account
import os

# def Upload_test_json():
# SA JSON for cred to GCS
key_path = os.path.join(os.path.expanduser('~'), '.semios', 'manufacturing_JSON_Upload_Aug22.json')
path = (os.getcwd()) + "\\wh132_json_files\\"  # Local path where JSON files are stored
gcs_bucket = 'manufacture_json_ingestion'  # GCS Bucket used in project
gcs_bucket_folder = 'prod/ALT_WH132/'  # Folder in GCS bucket to upload to
credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
gcs_client = storage.Client(
    credentials=credentials,
    project=credentials.project_id
)

def upload_json(filename):
    try:
        gcs_upload(filename)
        # move2uploaded(filename)
    except:
        print('Problem with uploading. Check internet connection')

def move2uploaded(filename):
    if not ("Uploaded" in os.listdir(path)):
        os.mkdir(path + "\\Uploaded")
    os.rename(path + "\\" + filename, path + "\\Uploaded\\" + filename)

def gcs_upload(filename):
    bucket = gcs_client.get_bucket(gcs_bucket)
    name_in_bucket = bucket.blob(gcs_bucket_folder + filename)
    name_in_bucket.upload_from_filename(path + filename)
    move2uploaded(filename)
    # print Fore.GREEN+"Json file is uploaded successfully"+Style.RESET_ALL
    # upload_json(filename)