# Rule Engine Configuration – Loading Guide

## For: Aniket (Fresher)

This guide will help you load all business rules into the ODOS Rule Engine. You can choose between two methods.

---

## Option A: Python Script (Easiest – Recommended)

### Step 1: Open Terminal

- **Windows**: Press `Windows Key + R`, type `cmd`, press Enter
- **Mac**: Press `Command + Space`, type `Terminal`, press Enter
- **Linux**: Press `Ctrl + Alt + T`

### Step 2: Navigate to the Folder

```
cd /path/to/rule_engine_config
```

*Replace `/path/to/rule_engine_config` with the actual folder location.*

**Example:**
```
cd C:\Users\Aniket\Downloads\rule_engine_config
```

### Step 3: Check Python is Installed

```
python --version
```

You should see something like:
```
Python 3.9.0
```

If you get an error, install Python from https://www.python.org/downloads/

### Step 4: Install Required Library (if needed)

```
pip install requests
```

### Step 5: Run the Script

```
python load_rules.py
```

### Step 6: Watch the Output

You should see something like:

```
============================================================
RULE ENGINE CONFIGURATION LOADER
============================================================

📁 Loading commission_rules.json...
   Found 3 commission rules
   Found 20 commission slabs

📁 Loading gst_tds_rules.json...
   Found 4 GST rules
   Found 9 TDS rules

📁 Loading validation_rules.json...
   Found 12 validation rules

✅ ALL RULES LOADED SUCCESSFULLY!

Summary:
   Commission Rules: 3
   Commission Slabs: 20
   GST Rules: 4
   TDS Rules: 9
   Validation Rules: 12
   Total: 48 rules

🎉 Done!
```

### Step 7: Done!

The rules are now loaded into the database. You can skip to the "Verification" section below.

---

## Option B: Swagger UI (Manual)

### Step 1: Open Swagger UI

1. Open your browser (Chrome, Firefox, or Edge)
2. Go to: `http://localhost:8000/docs`

You should see the Swagger UI page with all API endpoints.

### Step 2: Load Commission Rules

1. Scroll down to find the **POST** endpoint:
   ```
   POST /api/v1/rules/commission/bulk
   ```

2. Click on it to expand.

3. Click the **"Try it out"** button (blue button on the right).

4. Copy the ENTIRE content from `commission_rules.json` file.

5. Paste it into the **Request body** text box.

6. Click the **"Execute"** button (blue button at the bottom).

7. Look at the **Response** section. You should see:
   ```json
   {
     "status": "success",
     "rules_loaded": 3,
     "slabs_loaded": 20
   }
   ```

### Step 3: Load GST & TDS Rules

1. Find the **POST** endpoint:
   ```
   POST /api/v1/rules/tax/bulk
   ```

2. Click **"Try it out"**.

3. Copy the ENTIRE content from `gst_tds_rules.json`.

4. Paste it into the Request body.

5. Click **"Execute"**.

6. Check the response for success.

### Step 4: Load Validation Rules

1. Find the **POST** endpoint:
   ```
   POST /api/v1/rules/validation/bulk
   ```

2. Click **"Try it out"**.

3. Copy the ENTIRE content from `validation_rules.json`.

4. Paste it into the Request body.

5. Click **"Execute"**.

6. Check the response for success.

---

## Verification (Check That Rules Are Loaded)

### Method 1: Check via Swagger UI

1. In Swagger UI, find the **GET** endpoint:
   ```
   GET /api/v1/rules/commission
   ```

2. Click **"Try it out"**.

3. Click **"Execute"**.

4. You should see a list of all commission rules.

### Method 2: Check via Database

If you have database access, you can run:

```sql
SELECT COUNT(*) FROM RUL_CommissionRule;
SELECT COUNT(*) FROM RUL_CommissionSlab;
SELECT COUNT(*) FROM RUL_GSTRule;
SELECT COUNT(*) FROM RUL_TDSRule;
SELECT COUNT(*) FROM RUL_ValidationRule;
```

Expected counts:
- Commission Rules: 3+
- Commission Slabs: 20+
- GST Rules: 4
- TDS Rules: 9
- Validation Rules: 12

---

## Troubleshooting

### Error: "Connection refused"

**Solution:** Make sure the ODOS backend is running.

```
python main.py
```

Or check your Docker containers:

```
docker ps
```

### Error: "File not found"

**Solution:** Make sure you're in the correct folder.

```
cd /path/to/rule_engine_config
dir   # (Windows)
ls    # (Mac/Linux)
```

You should see all the JSON files.

### Error: "Duplicate key"

**Solution:** The rules may already be loaded. You can either:

1. Skip (rules already exist)
2. Delete existing rules first
3. Run with `--force` flag: `python load_rules.py --force`

### Error: "Invalid JSON"

**Solution:** Open the JSON file in a text editor and check:
- All brackets `{ }` and `[ ]` are balanced
- No trailing commas
- All keys are in double quotes

### Still Stuck?

Contact:
- CTO (ChatGPT) – Architecture Owner
- Technical Programme Manager (DeepSeek)
- Development Lead (Aniket)

---

## Summary

| Step | Action | Status |
|------|--------|--------|
| 1 | Open terminal / Swagger UI | ⬜ |
| 2 | Navigate to folder / find endpoint | ⬜ |
| 3 | Run script / paste JSON | ⬜ |
| 4 | Verify success | ⬜ |

---

**Good luck, Aniket! You've got this! 🚀**
