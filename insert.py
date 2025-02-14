"""
Script for seeding the database according to a pre-defined distribution.
Seeds tables: 'bin', 'assign_raccoon_clan', 'item_rummage' 
"""

from os import environ as ENV
from random import randint, choice

from dotenv import load_dotenv

from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor


def get_connection() -> connection:
    """Returns an open connection to the trash_pandas db."""
    return connect(
        database=ENV['DB_NAME'],
        host=ENV['DB_HOST'],
        user=ENV['DB_USER'],
        password=ENV['DB_PASSWORD'],
        port=ENV['DB_PORT']
    )


def get_bin_type_ids(conn: connection) -> dict[int, str]:
    """Returns a dictionary mapping bin type ids to type names."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM bin_type;")
        values = cur.fetchall()
    return {x['type_id']: x['type_name'] for x in values}


def get_city_ids(conn: connection) -> list[int]:
    """Returns a list of city IDs."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT city_id FROM city;")
        values = cur.fetchall()
    return [x['city_id'] for x in values]


def insert_bins(conn: connection, n=10):
    """Inserts randomly defined bins into the database."""
    bin_capacities = [randint(1, 20) * 10 for _ in range(n)]
    ease_of_accesses = [randint(1, 10) for _ in range(n)]
    type_map = get_bin_type_ids(conn)
    city_ids = get_city_ids(conn)

    with conn.cursor() as cur:
        for i in range(n):
            type_id = choice(list(type_map.keys()))
            city_id = choice(city_ids)
            capacity = bin_capacities[i]
            ease_of_access = ease_of_accesses[i]

            cur.execute("""
                INSERT INTO bin (city_id, type_id, 
                        capacity, ease_of_access)
                VALUES (%s, %s, %s, %s);
                """, (city_id, type_id, capacity, ease_of_access))
        conn.commit()


def insert_clans(conn: connection):
    pass


def insert_rummages(conn: connection):
    pass


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
    insert_bins(conn)
    insert_clans(conn)
    insert_rummages(conn)
