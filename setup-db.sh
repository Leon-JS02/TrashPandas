psql postgres -f schema.sql
python3 -m venv venv
source venv/bin/activate
python3 insert.py