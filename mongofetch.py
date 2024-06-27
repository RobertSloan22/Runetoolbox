def fetch_data_from_mongodb(client, db_name, collection_name, filter={}, project={}, max_retries=5):
    for attempt in range(max_retries):
        try:
            result = client[db_name][collection_name].find(filter, projection=project)
            data = list(result)
            return pd.DataFrame(data)
        except errors.ServerSelectionTimeoutError as err:
            print(f"Attempt {attempt + 1} failed: {err}")
            if attempt < max_retries - 1:
                time.sleep(5)  # wait for 5 seconds before retrying
            else:
                raise
