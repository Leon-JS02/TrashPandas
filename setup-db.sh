echo "Loading .env"
source .env

echo "Creating schema..."
psql -h $DB_HOST -U $DB_USER postgres -f schema.sql

echo "Creating virtual environment."
python3 -m venv venv
source venv/bin/activate

NUM=${1:-500}

echo "Seeding database with $NUM items."
python3 insert.py -n $NUM

echo "Setup complete!"