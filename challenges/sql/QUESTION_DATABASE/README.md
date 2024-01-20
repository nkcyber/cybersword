# SQL Question Database

This is a special directory that doesn't contain any questions, but just contains the shared database that the questions will reference.

- The SQLite3 database used for the questions will be created by [`seed_db.py`](./seed_db.py).
- The SQLite3 library comes with the standard Python Library.
    - [Docs](https://docs.python.org/3/library/sqlite3.html)

Both `db.sqlite` and `seed_db.sql` are shared with student.

We use singular naming conventions for table names, because I've found that to be more pedagogically grok-able (i.e. people understand it intuitively).

