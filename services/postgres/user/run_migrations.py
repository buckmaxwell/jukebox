#!/usr/bin/env python3

import os
import psycopg2
import sys

DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]

conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
)

migrations_dir_path = "/usr/src/app/user/migrations"
change_dir_path = os.path.join(migrations_dir_path, "change")
change_dir = os.fsencode(change_dir_path)


cur = conn.cursor()
cur.execute(
    """
create table if not exists __user_migrations__(
  id serial primary key,
  filename varchar,
  created_at timestamp default current_timestamp
)
"""
)
conn.commit()
cur.close()

try:
    cur = conn.cursor()
    cur.execute(
        "select filename from __user_migrations__ order by created_at desc limit 1"
    )
    last_run = cur.fetchone()[0]
except Exception as e:
    last_run = "00000000000.pgsql"

for _file in sorted(os.listdir(change_dir)):
    filename = os.fsdecode(_file)
    if filename.endswith(".pgsql") and filename > last_run:
        print("Running migration {}...".format(filename))
        cur = conn.cursor()
        cur.execute(open(os.path.join(change_dir_path, filename), "r").read().strip())
        conn.commit()
        cur.close()

        last_run = filename
        # important that it is here in case migration fails
        cur = conn.cursor()
        cur.execute(
            "insert into __user_migrations__(filename) values (%s)", (last_run,)
        )
        conn.commit()
        cur.close()

conn.close()
