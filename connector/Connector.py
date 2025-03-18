import pymongo


def connect_to_mongodb(host='localhost', port=27017, database=None, username=None, password=None, auth_source='admin'):
    try:
        if username and password:
            uri = f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource={auth_source}"
        else:
            uri = f"mongodb://{host}:{port}/"

        client = pymongo.MongoClient(uri)

        if database:
            db = client[database]
            print(f"Connected to MongoDB database: {database}")
            return db
        else:
            print("Connected to MongoDB server")
            return client
    except Exception as e:
        print(f"Could not establish a connection to MongoDB: {e}")
        return None
