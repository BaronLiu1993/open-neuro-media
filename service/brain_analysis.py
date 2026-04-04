from pathlib import Path

from tribev2 import TribeModel
from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os

load_dotenv()
mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
_model = None

# Get the model instance (singleton pattern)
def _get_model():
    global _model
    if _model is None:
        _model = TribeModel.from_pretrained("facebook/tribev2", cache_folder="./cache")
    return _model

# Get the MongoDB client
def get_mongo_write_client():
    uri = mongo_uri
    client = AsyncMongoClient(uri)
    return client


async def insert_data_to_db(preds, segments, source_name, user_id):
    client = get_mongo_write_client()
    db = client["neuro"]
    collection = db["predictions"]
    docs = [
        {
            "user_id": user_id,
            "source": source_name,
            "timepoint": float(segments[i].start),
            "duration": float(segments[i].duration),
            "activations": preds[i].tolist(),
        }
        for i in range(len(segments))
    ]
    result = await collection.insert_many(docs)
    return result.inserted_ids


def predict_from_text(text):
    model = _get_model()
    tmp = Path("./cache/input.txt")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(text)
    df = model.get_events_dataframe(text_path=str(tmp))
    preds, segments = model.predict(events=df)
    return preds, segments

def save_brain_analysis_results(source_name, user_id):
    preds, segments = predict_from_text(source_name)
    insert_data_to_db(preds, segments, source_name)
"""
if __name__ == "__main__":
    preds, segments = predict_from_video("/Users/baronliu/Desktop/project/neuro/service/test/news.mp4")
    print(preds)
"""
