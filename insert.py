"""
Script for seeding the database according to raccoon stats.
Seeds tables: 'bin', 'assign_raccoon_clan', 'item_rummage'
"""
from os import environ as ENV
from random import randint, choice, seed, choices
from datetime import datetime, timedelta
from argparse import ArgumentParser

from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from psycopg2 import connect
from dotenv import load_dotenv


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
        raccoons = cur.fetchall()
    return [{'id': x['raccoon_id'],
             'weight': x['weight'],
             'skill': x['rummaging_skill']} for x in raccoons]


def get_item_data(conn: connection) -> dict:
    """Returns a dictionary mapping item IDs to their edibility ratings."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT item_id, edibility FROM item;")
        items = cur.fetchall()
    return {x['item_id']: x['edibility'] for x in items}


def get_clan_ids(conn: connection) -> list[int]:
    """Returns a list of clan ids."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT clan_id FROM clan;")
        clans = cur.fetchall()
    return [x['clan_id'] for x in clans]


def get_rank_data(conn: connection) -> list[dict]:
    """Returns a list of rank objects, containing relevant data for seeding."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT rank_id, rank_seniority FROM rank;")
        ranks = cur.fetchall()
    return [{'id': x['rank_id'],
             'seniority': x['rank_seniority']} for x in ranks]


def get_bin_data(conn: connection) -> dict:
    """Returns a dictionary mapping bin IDs to their ease of access."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT bin_id, ease_of_access FROM bin;")
        bins = cur.fetchall()
    return {x['bin_id']: x['ease_of_access'] for x in bins}


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


def get_rummage_insert_lists(raccoons: list[dict],
                             bin_data: dict, item_data: dict, n=500) -> list[list]:
    """Generates a list of lists containing: raccoon IDs, bin IDs, item IDs dependent on criteria:
    - Heavier raccoons retrieve items with higher edibility.
    - Bins with a higher ease of access are represented more
    - Raccoons with higher skill are represented more."""
    raccoon_ids = [
        raccoon['id']
        for raccoon in raccoons
        for _ in range(raccoon['skill'])
    ]

    bin_ids = [
        bin_id
        for bin_id, ease_of_access in bin_data.items()
        for _ in range(ease_of_access)
    ]

    item_ids = []
    for raccoon in raccoons:
        raccoon_weight = raccoon['weight']
        weighted_items = [
            item_id
            for item_id, edibility in item_data.items()
            for _ in range(edibility * (raccoon_weight // 10))
        ]
        item_ids.extend(choices(weighted_items, k=1))

    bin_ids = choices(bin_ids, k=n)
    item_ids = choices(item_ids, k=n)
    raccoon_ids = choices(raccoon_ids, k=n)

    return [bin_ids, item_ids, raccoon_ids]


def generate_random_dates(n: int, interval: int = 7) -> list[datetime]:
    """Returns a list of n random dates within the past interval of days."""
    now = datetime.now()
    return [
        now - timedelta(days=randint(0, interval),
                        hours=randint(0, 23), minutes=randint(0, 59))
        for _ in range(n)
    ]


def insert_rummages(conn: connection, n=500):
    """Generates lists of bin_ids, item_ids, and raccoon_ids for inserting rummages in bulk."""
    raccoons = get_raccoon_data(conn)
    bin_data = get_bin_data(conn)
    item_data = get_item_data(conn)
    insert_lists = get_rummage_insert_lists(raccoons, bin_data, item_data, n)
    bin_ids = insert_lists[0]
    item_ids = insert_lists[1]
    raccoon_ids = insert_lists[2]
    rummage_dates = generate_random_dates(n)

    insert_stmt = """INSERT INTO item_rummage (item_id, raccoon_id, bin_id, rummaged_at)
                     VALUES (%s, %s, %s, %s);"""
    insert_values = [
        (item_ids[i], raccoon_ids[i], bin_ids[i],
         rummage_dates[i].strftime("%Y-%m-%d %H:%M:%S%z"))
        for i in range(n)
    ]

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.executemany(insert_stmt, insert_values)
    conn.commit()


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Insert rummaged items into the database.")
    parser.add_argument("-n", "--num", type=int, default=500,
                        help="Number of rummaged items to insert (default: 500)")
    args = parser.parse_args()

    seed(1)
    load_dotenv()
    db_conn = get_connection()
    insert_bins(db_conn)
    populate_clans(db_conn)
    insert_rummages(db_conn, args.num)
    db_conn.commit()
    db_conn.close()
