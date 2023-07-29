import random
from datetime import datetime, timedelta
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import RequestCount

rc_datetime = datetime(2023, 7, 27, 1, 30)
entry_num = 500
midl_na_cluster = "midl_na"
midl_eu_cluster = "midl_eu"
# Create an engine to establish a connection with the database
engine = create_engine(environ.get("SQLALCHEMY_DATABASE_URI"))
# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Flush tables
session.query(RequestCount).delete()

midl_na_rcs, midl_eu_rcs = [], []
for i in range(entry_num):
    rc_datetime += timedelta(seconds=600)
    count_na_num = random.randint(500, 100000)
    midl_na_rcs.append(
        RequestCount(
            count=count_na_num,
            cluster=midl_na_cluster,
            tick=rc_datetime,
        )
    )
    count_eu_num = random.randint(500, 100000)
    midl_eu_rcs.append(
        RequestCount(
            count=count_eu_num,
            cluster=midl_eu_cluster,
            tick=rc_datetime,
        )
    )

session.bulk_save_objects(midl_na_rcs)
session.bulk_save_objects(midl_eu_rcs)

session.commit()
session.close()
