# Trash Pandas DB
- A raccoon-themed database for learning SQL queries.

## Setup
**Prerequisites**
- `psql` installed on your device
- `python` installed on your device

**Steps**
1. Run `git clone <trash_pandas_url>`
2. Enter the repository and create a `.env` file with the following data:
```bash
DB_NAME=trash_pandas
DB_HOST=localhost
DB_PORT=5432
DB_USER=<XXXXXX>
DB_PASSWORD=<XXXXXX>
```
3. Enter the repository and run `bash setup-db.sh`
4. Create and activate a virtual environment
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`
5. Run `pip3 install -r requirements.txt`
6. Run `python3 insert.py`
