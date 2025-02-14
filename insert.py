"""
Script for seeding the database according to a pre-defined distribution.
Seeds tables: 'bin', 'assign_raccoon_clan', 'item_rummage' 
"""

from os import environ as ENV

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


def insert_bins(conn: connection):
    pass


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
