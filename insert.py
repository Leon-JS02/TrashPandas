"""
Script for seeding the database according to raccoon stats.
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


def get_raccoon_data(conn: connection) -> list[dict]:
    """Returns a list of raccoon objects containing relevant data for seeding."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""SELECT raccoon_id, weight, rummaging_skill
                    FROM raccoon;""")
        values = cur.fetchall()
    return [{'id': x['raccoon_id'],
             'weight': x['weight'],
             'skill': x['rummaging_skill']} for x in values]


def get_clan_ids(conn: connection) -> list[int]:
    """Returns a list of clan ids."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT clan_id FROM clan;")
        values = cur.fetchall()
    return [x['clan_id'] for x in values]


def get_rank_data(conn: connection) -> list[dict]:
    """Returns a list of rank objects, containing relevant data for seeding."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT rank_id, rank_seniority FROM rank;")
        ranks = cur.fetchall()
    return [{'id': x['rank_id'],
             'seniority': x['rank_seniority']} for x in ranks]


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


def populate_clans(conn: connection):
    """Evenly distributes the raccoons between the clans.
    Assigns their ranks based on their rummaging skill level."""

    clan_ids = get_clan_ids(conn)
    raccoon_data = sorted(get_raccoon_data(
        conn), key=lambda x: x['skill'], reverse=True)
    rank_map = {rank['seniority']: rank['id'] for rank in get_rank_data(conn)}

    raccoons_per_clan = len(raccoon_data) // len(clan_ids)
    remaining_raccoons = len(raccoon_data) % len(clan_ids)

    insert_stmt = """INSERT INTO assign_raccoon_clan 
                     (raccoon_id, clan_id, rank_id)
                     VALUES (%s, %s, %s);"""

    for i, raccoon in enumerate(raccoon_data):
        clan_index = (i // raccoons_per_clan) + (
            min(i // raccoons_per_clan, remaining_raccoons))
        rank_id = rank_map.get(raccoon['skill'])

        with conn.cursor() as cur:
            cur.execute(
                insert_stmt, (raccoon['id'], clan_ids[clan_index], rank_id))

    conn.commit()


def insert_rummages(conn: connection, n=500):
    """Inserts n rummage rows based on raccoon stats."""
    """
    Heavy raccoons will retrieve more edible items
    Low skilled raccoons will retrieve less total items
    """


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
    insert_bins(conn)
    populate_clans(conn)
    insert_rummages(conn)
    conn.commit()
    conn.close()
