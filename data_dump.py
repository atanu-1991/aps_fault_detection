import pymongo
import pandas as pd
import json

from sensor.config import mongo_client


# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

DATA_FILE_PATH = "/config/workspace/aps_failure_training_set1.csv"
DATABASE_NAME = "aps"
COLLECTION_NAME = "sensor"


if __name__ == "__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Roows and Columns: {df.shape}")

    # Convert data frame to json format so that we can dump this record into mongo db
    df.reset_index(drop=True,inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    # insert converted json record to mong db
    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)

