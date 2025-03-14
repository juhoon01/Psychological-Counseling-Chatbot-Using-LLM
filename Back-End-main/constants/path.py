import os

"""   Project Directory   """

PROJECT_DIR = os.getcwd()
ASSET_DIR = f'{PROJECT_DIR}/assets'
PROFILE_PHOTO_DIR = f'{PROJECT_DIR}/dataset/profile_photo'

for path in [ASSET_DIR, PROFILE_PHOTO_DIR]:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

"""   RAG   """
CSV_DATA_PATH = os.path.join(ASSET_DIR, 'knowledge_in_rag_data.csv')
VECTOR_DB_PATH = os.path.join(ASSET_DIR, 'vector_db')

for path in [CSV_DATA_PATH]:
    if not os.path.exists(path):
        raise FileNotFoundError(f'{path} is not found.')
