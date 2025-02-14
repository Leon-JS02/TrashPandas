echo "Loading .env"
source .env
echo "Creating schema..."
psql -h $DB_HOST -U $DB_USER postgres -f schema.sql
echo "Creating virtual environment."
python3 -m venv venv
source venv/bin/activate
echo "Seeding database."
python3 insert.py
echo "Setup complete!"