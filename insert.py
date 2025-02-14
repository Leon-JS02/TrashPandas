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


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
