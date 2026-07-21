# scripts/seed_test_data.py
"""
Optional: Populate test data for Master Data Management screens.
Run this script to insert sample Customers, Lenders, Products, Employees, and Connectors.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.masters.models import MST_Customer, MST_Lender, MST_Product, MST_Employee, MST_Connector


def seed_customers(db):
    customers = [
        {"full_name": "Rahul Sharma", "pan": "ABCDE1234F", "gstin": "22ABCDE1234F1Z5", "email": "rahul@example.com", "mobile": "9876543210"},
        {"full_name": "Priya Patel", "pan": "FGHIJ5678K", "gstin": "24FGHIJ5678K1Z6", "email": "priya@example.com", "mobile": "9876543211"},
        {"full_name": "Amit Kumar", "pan": "LMNOP9012Q", "gstin": "27LMNOP9012Q1Z7", "email": "amit@example.com", "mobile": "9876543212"},
    ]
    for data in customers:
        existing = db.query(MST_Customer).filter(MST_Customer.pan == data["pan"]).first()
        if not existing:
            customer = MST_Customer(**data, is_active=True)
            db.add(customer)
    db.commit()
    print(f"✅ Seeded {len(customers)} customers")


def seed_lenders(db):
    lenders = [
        {"lender_name": "HDFC Bank", "pan": "HDFC1234E", "gstin": "22HDFC1234E1Z1", "lender_code": "HDFC001", "is_nbfc": False},
        {"lender_name": "Axis Bank", "pan": "AXIS5678F", "gstin": "24AXIS5678F1Z2", "lender_code": "AXIS001", "is_nbfc": False},
        {"lender_name": "Tata Capital", "pan": "TATA9012G", "gstin": "27TATA9012G1Z3", "lender_code": "TATA001", "is_nbfc": True},
    ]
    for data in lenders:
        existing = db.query(MST_Lender).filter(MST_Lender.pan == data["pan"]).first()
        if not existing:
            lender = MST_Lender(**data, is_active=True)
            db.add(lender)
    db.commit()
    print(f"✅ Seeded {len(lenders)} lenders")


def seed_products(db):
    products = [
        {"product_name": "Home Loan", "product_code": "HL001", "lender_id": 1, "interest_rate": 8.5, "min_loan_amount": 500000, "max_loan_amount": 5000000},
        {"product_name": "Personal Loan", "product_code": "PL001", "lender_id": 2, "interest_rate": 10.5, "min_loan_amount": 100000, "max_loan_amount": 2500000},
        {"product_name": "Business Loan", "product_code": "BL001", "lender_id": 3, "interest_rate": 12.0, "min_loan_amount": 200000, "max_loan_amount": 10000000},
    ]
    for data in products:
        existing = db.query(MST_Product).filter(MST_Product.product_code == data["product_code"]).first()
        if not existing:
            product = MST_Product(**data, is_active=True)
            db.add(product)
    db.commit()
    print(f"✅ Seeded {len(products)} products")


def seed_employees(db):
    employees = [
        {"employee_code": "EMP001", "full_name": "Sanjay Mehta", "designation": "Branch Manager", "department": "Sales", "email": "sanjay@odos.com", "mobile": "9876543213"},
        {"employee_code": "EMP002", "full_name": "Neha Gupta", "designation": "Relationship Manager", "department": "Sales", "email": "neha@odos.com", "mobile": "9876543214"},
        {"employee_code": "EMP003", "full_name": "Vikram Singh", "designation": "Operations Executive", "department": "Operations", "email": "vikram@odos.com", "mobile": "9876543215"},
    ]
    for data in employees:
        existing = db.query(MST_Employee).filter(MST_Employee.employee_code == data["employee_code"]).first()
        if not existing:
            employee = MST_Employee(**data, is_active=True)
            db.add(employee)
    db.commit()
    print(f"✅ Seeded {len(employees)} employees")


def seed_connectors(db):
    connectors = [
        {"connector_code": "CON001", "full_name": "Dinesh Agarwal", "pan": "DINE1234A", "gstin": "22DINE1234A1Z4", "bank_name": "SBI", "account_number": "1234567890", "ifsc": "SBIN0012345"},
        {"connector_code": "CON002", "full_name": "Sneha Reddy", "pan": "SNEH5678B", "gstin": "24SNEH5678B1Z5", "bank_name": "HDFC", "account_number": "0987654321", "ifsc": "HDFC0012345"},
        {"connector_code": "CON003", "full_name": "Mahesh Patel", "pan": "MAHE9012C", "gstin": "27MAHE9012C1Z6", "bank_name": "ICICI", "account_number": "5678901234", "ifsc": "ICIC0012345"},
    ]
    for data in connectors:
        existing = db.query(MST_Connector).filter(MST_Connector.connector_code == data["connector_code"]).first()
        if not existing:
            connector = MST_Connector(**data, is_active=True)
            db.add(connector)
    db.commit()
    print(f"✅ Seeded {len(connectors)} connectors")


if __name__ == "__main__":
    db = SessionLocal()
    print("🌱 Seeding test data...")
    seed_customers(db)
    seed_lenders(db)
    seed_products(db)
    seed_employees(db)
    seed_connectors(db)
    db.close()
    print("✅ All test data seeded successfully!")
