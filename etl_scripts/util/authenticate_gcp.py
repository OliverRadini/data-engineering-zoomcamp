from google.cloud import storage

def authenticate_gcp(project_id):
    _ = storage.Client(project=project_id)
    print("Authentication confirmed")
