import psycopg
import json

conn_str = "postgresql://postgres:password@192.168.1.194:5432/postgres"

json_raw = None

with open(r"./jobs.json", "r") as f:
    json_raw = json.loads(f.read())

raws = [(json.dumps(d),) for d in json_raw]


with psycopg.connect(conn_str) as conn:
    with conn.cursor() as cur:
        cur.executemany("INSERT INTO json_raw values (Now(),%s::jsonb)", raws)
