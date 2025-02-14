"""
Script for seeding the database according to a pre-defined distribution.
Seeds tables: 'bin', 'assign_raccoon_clan', 'item_rummage' 
"""

from dotenv import load_dotenv

from psycopg2 import connect
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor

if __name__ == "__main__":
    load_dotenv()
