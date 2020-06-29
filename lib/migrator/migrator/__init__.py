#!/usr/bin/env/python3

import os
import psycopg2
import sys

DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]


def run_migrations(schema):
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )
    migrations_dir_path = f"/usr/src/app/{schema}/migrations"
    change_dir_path = os.path.join(migrations_dir_path, "change")
    change_dir = os.fsencode(change_dir_path)

    cur = conn.cursor()
    cur.execute(
        f"""
    create table if not exists __{schema}_migrations__(
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
            f"select filename from __{schema}_migrations__ order by created_at desc limit 1"
        )
        last_run = cur.fetchone()[0]
    except Exception:
        last_run = "00000000000.pgsql"

    for _file in sorted(os.listdir(change_dir)):
        filename = os.fsdecode(_file)
        if filename.endswith(".pgsql") and filename > last_run:
            print("Running migration {}...".format(filename))
            cur = conn.cursor()
            cur.execute(
                open(os.path.join(change_dir_path, filename), "r").read().strip()
            )
            conn.commit()
            cur.close()

            last_run = filename
            # important that it is here in case migration fails
            cur = conn.cursor()
            cur.execute(
                f"insert into __{schema}_migrations__(filename) values (%s)",
                (last_run,),
            )
            conn.commit()
            cur.close()

    conn.close()


def rollback_migrations(schema):
    migrations_dir_path = f"/usr/src/app/{schema}/migrations"
    rollback_dir_path = os.path.join(migrations_dir_path, "rollback")
    rollback_dir = os.fsencode(rollback_dir_path)

    # roll back all migrations to (and including) target migration
    # No arguments rolls back last migration
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )

    cur = conn.cursor()
    cur.execute(
        f"""
    create table if not exists __{schema}_migrations__(
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
            f"select filename from __{schema}_migrations__ order by created_at desc limit 1"
        )
        last_run = cur.fetchone()[0]
    except Exception:
        last_run = "00000000000.pgsql"

    current_version = last_run

    try:
        target = sys.argv[1]
    except IndexError:
        target = current_version

    print(target)

    rollback_files = sorted(os.listdir(rollback_dir), reverse=True)
    for i, _file in enumerate(rollback_files):
        filename = os.fsdecode(_file)
        if (
            filename.endswith(".pgsql")
            and filename >= target
            and filename <= current_version
        ):
            print("Rolling back {}...".format(filename))
            cur = conn.cursor()
            cur.execute(open(os.path.join(rollback_dir_path, filename), "r").read())
            conn.commit()
            cur.close()

            try:
                last_run = os.fsdecode(rollback_files[i + 1])
            except IndexError:
                last_run = "00000000000.pgsql"
            # important that it is here in case migration fails
            cur = conn.cursor()
            cur.execute(
                f"insert into __{schema}_migrations__(filename) values (%s)",
                (last_run,),
            )
            conn.commit()
            cur.close()

    conn.close()


__version__ = "0.0.1"
