# Data Reset and Archive Guide

## Why this exists
Use this when you need to start fresh while preserving an audit copy of current data.

## Script
- scripts/archive_and_reset_data.py

## Modes
1. Archive only (safe default)
- python scripts/archive_and_reset_data.py --mode archive

2. Reset only (destructive)
- python scripts/archive_and_reset_data.py --mode reset --confirm

3. Archive then reset (recommended)
- python scripts/archive_and_reset_data.py --mode archive-reset --confirm

## What gets archived/reset
- Masters: customer, lender, product, employee, connector, vendor, expense category, cost center, company bank account
- Transactions: case, revenue, commission, expense, payment, recurring expense, expense claim, tally export batch/detail
- Rules/tax: validation, commission, slabs, gst, tds
- ETL: import batch, staging, errors, lineage

## Where archive is stored
- Default folder: archives/
- Default file format: odos_archive_YYYYMMDD_HHMMSS.json

## Notes
- This operation removes data rows only, not schema.
- Keep the archive file before destructive reset.
- If you need metadata templates retained, use archive mode and then selectively delete tables manually.
