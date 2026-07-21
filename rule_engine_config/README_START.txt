╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   RULE ENGINE CONFIGURATION LOADER                               ║
║   For: Aniket (Fresher Friendly)                                 ║
║   Version: 1.0                                                   ║
║   Date: July 2026                                                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝


📋 WHAT THIS PACKAGE DOES
==========================
This package loads all business rules (Commission, GST, TDS, Validation)
into the ODOS Rule Engine database.

You have TWO OPTIONS to load the rules. Choose the one you're most
comfortable with:

    OPTION A (EASIEST): Run the Python script
    OPTION B (MANUAL): Use the Swagger UI in your browser


🚀 OPTION A – RUN THE PYTHON SCRIPT (Recommended)
==================================================
This is the easiest way. Just open your terminal and run:

    cd /path/to/rule_engine_config
    python load_rules.py

That's it! The script will:
    1. Check if your database is running
    2. Load all JSON files
    3. Show you what was loaded
    4. Confirm success

No manual steps required.


🌐 OPTION B – USE SWAGGER UI (Manual)
======================================
Prefer clicking buttons? Use Swagger UI:

    1. Open your browser: http://localhost:8000/docs
    2. Find the POST endpoints under "Rules"
    3. Copy-paste the JSON from the files provided
    4. Click "Execute"

See load_instructions.md for detailed screenshots and steps.


📁 FILES INCLUDED
==================
├── README_START.txt          ← You are here
├── load_instructions.md      ← Detailed step-by-step guide
├── load_rules.py             ← Python loader script (Option A)
├── commission_rules.json     ← Commission rules (RUL_CommissionRule)
├── gst_tds_rules.json        ← GST & TDS rules (RUL_GSTRule, RUL_TDSRule)
└── validation_rules.json     ← Validation rules (RUL_ValidationRule)


✅ CHECKLIST – Before You Start
================================
[ ] Make sure your ODOS backend is running
[ ] Make sure the database is accessible
[ ] Make sure you have Python installed (if using Option A)
[ ] Make sure you have the correct file path


⚠️ TROUBLESHOOTING
===================
If you get errors:

1. "Connection refused" → Make sure the backend is running
2. "File not found" → Make sure you're in the correct folder
3. "Duplicate key error" → Rules already exist, run with --force flag

If you're stuck, contact the CTO or your team lead.


📞 SUPPORT
===========
CTO (ChatGPT) - Architecture Owner
Technical Programme Manager (DeepSeek)
Development Lead (Aniket)


GOOD LUCK! 🎉
