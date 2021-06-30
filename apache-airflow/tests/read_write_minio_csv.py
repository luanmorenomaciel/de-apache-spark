# import libraries
import pandas as pd
from minio import Minio
from io import BytesIO

# pandas config
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# set up connectivity with minio storage
# minio.deepstorage.svc.Cluster.local:9000
client = Minio("localhost:9000", "YOURACCESSKEY", "YOURSECRETKEY", secure=False)

# download file from bucket
obj_business = client.get_object(
    "processing",
    "business/yelp_business.json",
)

# read json file using pandas
# select and output only 10 rows
df_business = pd.read_json(obj_business, lines=True)
selected_data = df_business[["business_id", "name", "city", "state", "stars", "review_count"]].head(10)

# dataframe to csv - encode and buffer bytes
csv_bytes = selected_data.to_csv(header=False, index=False).encode('utf-8')
csv_buffer = BytesIO(csv_bytes)

# writing into minio storage
# csv file without header
client.put_object(
    "curated",
    "business/yelp_business.csv",
    data=csv_buffer,
    length=len(csv_bytes),
    content_type='application/csv')