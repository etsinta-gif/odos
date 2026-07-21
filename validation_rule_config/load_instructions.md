# Validation Rules – Loading Guide

## For: Aniket (Fresher)

This guide will help you load all validation rules into the ODOS Rule Engine. You can choose between two methods.

---

## Option A: Python Script (Easiest – Recommended)

### Step 1: Open Terminal

- **Windows**: Press `Windows Key + R`, type `cmd`, press Enter
- **Mac**: Press `Command + Space`, type `Terminal`, press Enter
- **Linux**: Press `Ctrl + Alt + T`

### Step 2: Navigate to the Folder

```
cd /path/to/validation_rule_config
```

*Replace `/path/to/validation_rule_config` with the actual folder location.*

**Example:**
```
cd C:\Users\Aniket\Downloads\validation_rule_config
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
VALIDATION RULE ENGINE - CONFIGURATION LOADER
============================================================

ℹ️  API URL: http://localhost:8000/api/v1
ℹ️  Checking if API is reachable...
✅ API is reachable!

============================================================
Loading Validation Rules
============================================================
✅ Loaded validation_rules.json
ℹ️  Found 13 validation rules
✅ Validation Rules loaded successfully!

============================================================
LOAD COMPLETE
============================================================
✅ ALL RULES LOADED SUCCESSFULLY! 🎉

Summary:
  ✅ validation_rules.json

Next Steps:
1. Verify rules are loaded by checking the database
2. Run a test case to validate rule execution
3. Notify the CTO that rules are loaded
4. Proceed to Phase 4 development

🎉 Done!
```

### Step 7: Done!

The rules are now loaded into the database. Skip to "Testing Your Rules" below.

---

## Option B: Swagger UI (Manual)

### Step 1: Open Swagger UI

1. Open your browser (Chrome, Firefox, or Edge)
2. Go to: `http://localhost:8000/docs`

You should see the Swagger UI page with all API endpoints.

### Step 2: Load Validation Rules

1. Scroll down to find the **POST** endpoint:
   ```
   POST /api/v1/rules/validation/bulk
   ```

2. Click on it to expand.

3. Click the **"Try it out"** button (blue button on the right).

4. Copy the ENTIRE content from `validation_rules.json` file.

5. Paste it into the **Request body** text box.

6. Click the **"Execute"** button (blue button at the bottom).

7. Look at the **Response** section. You should see:
   ```json
   {
     "status": "success",
     "rules_loaded": 13
   }
   ```

### Step 3: Done!

The rules are now loaded into the database.

---

## Testing Your Rules

### Method 1: Test with Sample Data

You can use the `sample_test_data.json` file to test if validation rules work.

#### Using Swagger UI:

1. Find the **POST** endpoint for validation testing:
   ```
   POST /api/v1/rules/validation/test
   ```

2. Click **"Try it out"**.

3. Copy the content from `sample_test_data.json`.

4. Paste it into the Request body.

5. Click **"Execute"**.

6. You should see which records PASS or FAIL validation.

#### Expected Results:

```json
{
  "results": [
    {
      "record_id": 1,
      "passed": true,
      "errors": []
    },
    {
      "record_id": 2,
      "passed": false,
      "errors": [
        {
          "rule": "VAL-PAN-001",
          "message": "PAN must be 10 characters: 5 letters, 4 digits, 1 letter",
          "severity": "CRITICAL"
        }
      ]
    },
    {
      "record_id": 3,
      "passed": true,
      "errors": []
    }
  ]
}
```

### Method 2: Test with Live Data

When you import actual data, validation rules will automatically run. You'll see validation errors in the `ETL_ErrorLog` table.

### Method 3: Check Rules in Database

If you have database access, you can run:

```sql
SELECT COUNT(*) FROM RUL_ValidationRule;
-- Expected: 13

SELECT RuleCode, RuleName, Severity FROM RUL_ValidationRule ORDER BY RuleCode;
```

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
cd /path/to/validation_rule_config
dir   # (Windows)
ls    # (Mac/Linux)
```

You should see all the files.

### Error: "Duplicate key"

**Solution:** The rules may already be loaded. You can either:

1. Skip (rules already exist)
2. Delete existing rules first
3. Run with `--force` flag: `python load_rules.py --force`

### Error: "Invalid JSON"

**Solution:** Open `validation_rules.json` in a text editor and check:
- All brackets `{ }` and `[ ]` are balanced
- No trailing commas
- All keys are in double quotes

### Error: "Validation rule execution failed"

**Solution:** Check the error message. Common issues:
- Rule expression has syntax error
- Field name doesn't exist in schema
- Referenced table doesn't exist

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
| 4 | Test with sample data | ⬜ |
| 5 | Verify rules loaded | ⬜ |

---

**You're a rockstar, Aniket! 🌟**
