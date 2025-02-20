# 🦝 Trash Pandas DB 🦝
- A raccoon-themed database for learning SQL queries.



## Setup
**Prerequisites**
- `psql` installed on your device
- `python3` installed on your device
- `git` installed on your device

**Steps**
1. Run `git clone https://github.com/Leon-JS02/TrashPandas`
2. Enter the repository and create a `.env` file with the following data:
```bash
DB_NAME=trash_pandas
DB_HOST=localhost
DB_PORT=5432
DB_USER=<XXXXXX>
DB_PASSWORD=<XXXXXX>
```
3. Run `bash setup-db.sh [n: int, default = 500]`

    e.g. `bash setup-db.sh 10000`

## ERD

![Trash Pandas ERD](erd.png)
