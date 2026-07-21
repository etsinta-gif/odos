# FCPL Data Load – Step-by-Step Guide for Aniket

This guide will walk you through loading the three FCPL Excel files into the staging tables of the ODOS development database.

**Estimated time:** 30 minutes

---

## Before You Start

- You have completed **Phase 1** of the ODOS project.
- Your database is running (PostgreSQL).
- You have the Excel files (Connector Master, Lender Payout, Secured Tracker) saved on your computer.

---

## Step 0: Verify Staging Tables Exist

**What to do:** Check that your database has the required staging tables. The import scripts need these tables to be present.

You can do this using the Swagger UI (the API documentation page) or by running a simple SQL query.

### Option A: Using Swagger UI (Recommended)

1. Open your browser and go to: `http://localhost:8000/docs`
2. Scroll down to the **ETL** section and find the endpoint: `GET /api/v1/etl/batches`
3. Click on it to expand it, then click **"Try it out"**.
4. Click **"Execute"**.

**Expected result:**
```
{
  "status": "success",
  "data": []
}
```
*An empty list means the tables exist and are ready. The data will be empty because you haven't imported anything yet.*

**If you see `404 Not Found` or `Internal Server Error`:**
- The database may not have the staging tables. Run the migrations:
  ```bash
  alembic upgrade head
  ```
- Then restart the server:
  ```bash
  uv run uvicorn src.main:app --reload
  ```
- Refresh Swagger and try again.

### Option B: Using SQL (if you have psql or pgAdmin)

1. Open pgAdmin or your SQL client.
2. Run this query:

```sql
SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename LIKE 'etl_staging%';
```

**Expected result:** You should see at least these tables:
- `etl_importbatch`
- `etl_staging_connectormaster`
- `etl_staging_lenderpayout`
- `etl_staging_securedtracker`
- `etl_errorlog`

If you see any missing, run the migrations as shown in Option A.

---

## Step 1: Open VS Code and Navigate to the Project Folder

**What to do:** Open your project in VS Code.

1. Open **VS Code**.
2. Click **File → Open Folder**.
3. Navigate to your ODOS project folder.  
   Example: `C:\Users\etsin\OneDrive\Documents\AI Projects\ODOS Test\odos`
4. Click **Select Folder**.

**What to expect:** You should see the project files in the left sidebar.

---

## Step 2: Create a Virtual Environment (if not already done)

**What to do:** Open the terminal in VS Code.

- Click **Terminal → New Terminal**.
- A terminal window will open at the bottom.

**Command:**

```bash
python -m venv venv
```

**What to expect:** A new folder named `venv` will appear in your project.

---

## Step 3: Activate the Virtual Environment

**What to do:** Activate the environment so that installed packages are available.

- **On Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **On Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

**What to expect:** Your terminal prompt will show `(venv)` at the beginning.

**If it fails:** Make sure you are in the project root folder. If you get an error about execution policy on Windows, run:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try again.

---

## Step 4: Install Required Python Packages

**What to do:** Install the packages needed to run the scripts.

**Command:**

```bash
pip install -r requirements.txt
```

**If you don't have `requirements.txt`**, use this command instead:

```bash
pip install pandas openpyxl psycopg2-binary python-dotenv
```

**What to expect:** You will see a lot of text scrolling – that's normal. Wait until it finishes.

---

## Step 5: Set Up Environment Variables (Database Connection)

**What to do:** Create a `.env` file in the project root with your database credentials.

1. In VS Code, right-click in the file explorer and choose **New File**.
2. Name it **`.env`** (exactly like that – with the dot at the beginning).
3. Copy the contents from the file `.env.example` (included in this folder) and paste it into `.env`.
4. Replace the placeholder values with your actual database details.

**Example `.env` file:**

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=odos_dev
DB_USER=postgres
DB_PASSWORD=your_password
```

**What to expect:** Nothing visible, but the scripts will use these values to connect.

---

## Step 6: Place the Excel Files in the `data/` Folder

**What to do:** Create a folder called `data` inside your project root (if it doesn't exist). Then copy the three Excel files into it.

1. In VS Code, right-click in the file explorer and choose **New Folder** – name it `data`.
2. Open File Explorer (Windows) or Finder (Mac).
3. Navigate to where you have the Excel files.
4. Copy the following files and paste them into the `data` folder:
   - `Connector Master.xlsx` (or similar name)
   - `FCPL Lender Payout Data.xlsx`
   - `Secured Tracker FY 26-27 (2).xlsx`

**What to expect:** Your `data` folder should now contain those three files.

**Note:** If your file names are different, you will need to adjust the command in Step 7 accordingly.

---

## Step 7: Run the Import Scripts

### 7.1 Import Connector Master

**What to do:** Run the script for Connector Master.

**Command:**

```bash
python import_connector_master.py
```

**What to expect (success):**

```
============================================================
FCPL Data Load – Connector Master
============================================================
[INFO] Reading file: data/Connector Master.xlsx
[INFO] Creating import batch...
[INFO] Batch created: BATCH-1234-5678-90ab-cdef
[INFO] Parsing 2966 rows...
[INFO] Inserted 2966 records into ETL_Staging_ConnectorMaster.
[INFO] Batch status updated to STAGED.
[INFO] Done.
```

**If you see an error:** Check the Troubleshooting section below.

---

### 7.2 Import Lender Payout Data

**What to do:** Run the script for Lender Payout.

**Command:**

```bash
python import_lender_payout.py
```

**What to expect (success):**

```
============================================================
FCPL Data Load – Lender Payout
============================================================
[INFO] Reading file: data/FCPL Lender Payout Data.xlsx
[INFO] Creating import batch...
[INFO] Batch created: BATCH-9876-5432-10ab-cdef
[INFO] Parsing 230 rows...
[INFO] Inserted 230 records into ETL_Staging_LenderPayout.
[INFO] Batch status updated to STAGED.
[INFO] Done.
```

---

### 7.3 Import Secured Tracker

**What to do:** Run the script for Secured Tracker.

**Command:**

```bash
python import_secured_tracker.py
```

**What to expect (success):**

```
============================================================
FCPL Data Load – Secured Tracker
============================================================
[INFO] Reading file: data/Secured Tracker FY 26-27 (2).xlsx
[INFO] Creating import batch...
[INFO] Batch created: BATCH-1111-2222-3333-4444
[INFO] Parsing 384 rows...
[INFO] Inserted 384 records into ETL_Staging_SecuredTracker.
[INFO] Batch status updated to STAGED.
[INFO] Done.
```

---

## Step 8: Verify the Data in the Database

**What to do:** Check that the staging tables contain the data.

**Command:** (in terminal, if you have `psql` installed)

```bash
psql -U postgres -d odos_dev -c "SELECT COUNT(*) FROM ETL_Staging_ConnectorMaster;"
psql -U postgres -d odos_dev -c "SELECT COUNT(*) FROM ETL_Staging_LenderPayout;"
psql -U postgres -d odos_dev -c "SELECT COUNT(*) FROM ETL_Staging_SecuredTracker;"
```

**What to expect:** The counts should match the number of rows in each Excel file.

Alternatively, you can use pgAdmin or DBeaver to run these queries.

---

## 🛠️ Troubleshooting Common Errors

| Error | Likely Cause | How to Fix |
|-------|--------------|------------|
| `ModuleNotFoundError: No module named 'pandas'` | Package not installed | Run `pip install pandas` |
| `ModuleNotFoundError: No module named 'openpyxl'` | Package not installed | Run `pip install openpyxl` |
| `ModuleNotFoundError: No module named 'psycopg2'` | Package not installed | Run `pip install psycopg2-binary` |
| `FileNotFoundError: [Errno 2] No such file or directory: 'data/...'` | Excel file missing or wrong name | Check that the file exists in `data/` and the name matches the script's expectation. You can update the script to the correct filename. |
| `psycopg2.OperationalError: connection to server failed` | Database not running or wrong credentials | Check that PostgreSQL is running. Verify `.env` credentials. |
| `PermissionError: [WinError 5] Access is denied` | File is open in Excel | Close the Excel file and run again. |
| `ValueError: Excel file format cannot be determined` | File is corrupted or not an Excel file | Try re-saving the file as `.xlsx`. |
| `psycopg2.errors.UndefinedTable: relation "etl_importbatch" does not exist` | Staging tables not created | Run Step 0 – you need to run `alembic upgrade head` first. |

---

## 🔄 If Something Goes Wrong – Re-run

If a script fails, you can fix the issue and run it again. The script will **not** insert duplicate batches because each run creates a new batch.

---

## ✅ Completion Checklist

- [ ] Step 0 – Verified staging tables exist
- [ ] Opened VS Code and project folder
- [ ] Created and activated virtual environment
- [ ] Installed required packages
- [ ] Created `.env` file with database credentials
- [ ] Placed Excel files in `data/`
- [ ] Ran `import_connector_master.py` (success)
- [ ] Ran `import_lender_payout.py` (success)
- [ ] Ran `import_secured_tracker.py` (success)
- [ ] Verified counts in database

---

## 📞 Need Help?

If you still have problems, take a screenshot of the error and send it to the CTO.

**Congratulations!** You have loaded the FCPL staging data. 🎉
