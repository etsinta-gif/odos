# Alembic Migration Setup

This project uses Alembic for database schema migrations.

To create a new migration:

```bash
alembic revision --autogenerate -m "add_tally_tables"
```

To apply migrations:

```bash
alembic upgrade head
```
