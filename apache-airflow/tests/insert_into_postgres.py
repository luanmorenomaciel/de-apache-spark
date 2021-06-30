# import libraries
import pandas as pd
from minio import Minio
from sqlalchemy import create_engine

# set up connectivity with minio storage
# minio.deepstorage.svc.Cluster.local:9000
client = Minio("localhost:9000", "YOURACCESSKEY", "YOURSECRETKEY", secure=False)

# download file from bucket
obj_business = client.get_object("curated", "business/yelp_business.csv")

# read file from curated zone
df_business = pd.read_csv(obj_business).head(1000)
print(df_business)

# insert pandas data frame into postgres db [sqlalchemy]
# postgresql://yugabyte:yugabyte@yb-tservers.database.svc.Cluster.local:5433/owshq
postgres_engine = create_engine('postgresql://yugabyte:yugabyte@localhost:5433/owshq')
df_business.to_sql('business', postgres_engine, if_exists='append', index=False, chunksize=10)
