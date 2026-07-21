# src/masters/ui/routes.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.masters.models import MST_Customer, MST_Lender, MST_Product, MST_Employee, MST_Connector
from src.main import templates

router = APIRouter(prefix="/masters", tags=["UI"])

# CUSTOMER UI ROUTES
@router.get("/customers")
async def customer_list(request: Request, db: Session = Depends(get_db)):
    customers = db.query(MST_Customer).filter(MST_Customer.is_active == True).all()
    return templates.TemplateResponse(
        "masters/customer_list.html",
        {"request": request, "customers": customers}
    )

@router.get("/customers/add")
async def customer_add_form(request: Request):
    return templates.TemplateResponse(
        "masters/customer_form.html",
        {"request": request, "customer": None, "action": "add"}
    )

@router.post("/customers")
async def customer_create(
    request: Request,
    full_name: str = Form(...),
    pan: str = Form(...),
    gstin: str = Form(None),
    email: str = Form(None),
    mobile: str = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.customer import create_customer, CustomerCreate
    customer_data = CustomerCreate(
        full_name=full_name,
        pan=pan,
        gstin=gstin,
        email=email,
        mobile=mobile
    )
    create_customer(customer_data, db)
    return RedirectResponse(url="/masters/customers", status_code=303)

@router.get("/customers/{customer_id}/edit")
async def customer_edit_form(request: Request, customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(MST_Customer).filter(MST_Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return templates.TemplateResponse(
        "masters/customer_form.html",
        {"request": request, "customer": customer, "action": "edit"}
    )

@router.post("/customers/{customer_id}/edit")
async def customer_update(
    request: Request,
    customer_id: int,
    full_name: str = Form(...),
    pan: str = Form(...),
    gstin: str = Form(None),
    email: str = Form(None),
    mobile: str = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.customer import update_customer, CustomerUpdate
    customer_data = CustomerUpdate(
        full_name=full_name,
        pan=pan,
        gstin=gstin,
        email=email,
        mobile=mobile
    )
    update_customer(customer_id, customer_data, db)
    return RedirectResponse(url="/masters/customers", status_code=303)

@router.get("/customers/{customer_id}/delete")
async def customer_delete(customer_id: int, db: Session = Depends(get_db)):
    from src.masters.api.customer import delete_customer
    delete_customer(customer_id, db)
    return RedirectResponse(url="/masters/customers", status_code=303)

# LENDER UI ROUTES
@router.get("/lenders")
async def lender_list(request: Request, db: Session = Depends(get_db)):
    lenders = db.query(MST_Lender).filter(MST_Lender.is_active == True).all()
    return templates.TemplateResponse(
        "masters/lender_list.html",
        {"request": request, "lenders": lenders}
    )

@router.get("/lenders/add")
async def lender_add_form(request: Request):
    return templates.TemplateResponse(
        "masters/lender_form.html",
        {"request": request, "lender": None, "action": "add"}
    )

@router.post("/lenders")
async def lender_create(
    request: Request,
    lender_name: str = Form(...),
    pan: str = Form(...),
    gstin: str = Form(None),
    lender_code: str = Form(None),
    is_nbfc: bool = Form(False),
    credit_rating: str = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.lender import create_lender, LenderCreate
    lender_data = LenderCreate(
        lender_name=lender_name,
        pan=pan,
        gstin=gstin,
        lender_code=lender_code,
        is_nbfc=is_nbfc,
        credit_rating=credit_rating
    )
    create_lender(lender_data, db)
    return RedirectResponse(url="/masters/lenders", status_code=303)

@router.get("/lenders/{lender_id}/edit")
async def lender_edit_form(request: Request, lender_id: int, db: Session = Depends(get_db)):
    lender = db.query(MST_Lender).filter(MST_Lender.lender_id == lender_id).first()
    if not lender:
        raise HTTPException(status_code=404, detail="Lender not found")
    return templates.TemplateResponse(
        "masters/lender_form.html",
        {"request": request, "lender": lender, "action": "edit"}
    )

@router.post("/lenders/{lender_id}/edit")
async def lender_update(
    request: Request,
    lender_id: int,
    lender_name: str = Form(...),
    pan: str = Form(...),
    gstin: str = Form(None),
    lender_code: str = Form(None),
    is_nbfc: bool = Form(False),
    credit_rating: str = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.lender import update_lender, LenderUpdate
    lender_data = LenderUpdate(
        lender_name=lender_name,
        pan=pan,
        gstin=gstin,
        lender_code=lender_code,
        is_nbfc=is_nbfc,
        credit_rating=credit_rating
    )
    update_lender(lender_id, lender_data, db)
    return RedirectResponse(url="/masters/lenders", status_code=303)

@router.get("/lenders/{lender_id}/delete")
async def lender_delete(lender_id: int, db: Session = Depends(get_db)):
    from src.masters.api.lender import delete_lender
    delete_lender(lender_id, db)
    return RedirectResponse(url="/masters/lenders", status_code=303)

# PRODUCT UI ROUTES
@router.get("/products")
async def product_list(request: Request, db: Session = Depends(get_db)):
    products = db.query(MST_Product).filter(MST_Product.is_active == True).all()
    return templates.TemplateResponse(
        "masters/product_list.html",
        {"request": request, "products": products}
    )

@router.get("/products/add")
async def product_add_form(request: Request):
    return templates.TemplateResponse(
        "masters/product_form.html",
        {"request": request, "product": None, "action": "add"}
    )

@router.post("/products")
async def product_create(
    request: Request,
    product_name: str = Form(...),
    product_code: str = Form(None),
    lender_id: int = Form(None),
    interest_rate: float = Form(None),
    min_loan_amount: float = Form(None),
    max_loan_amount: float = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.product import create_product, ProductCreate
    product_data = ProductCreate(
        product_name=product_name,
        product_code=product_code,
        lender_id=lender_id,
        interest_rate=interest_rate,
        min_loan_amount=min_loan_amount,
        max_loan_amount=max_loan_amount
    )
    create_product(product_data, db)
    return RedirectResponse(url="/masters/products", status_code=303)

@router.get("/products/{product_id}/edit")
async def product_edit_form(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = db.query(MST_Product).filter(MST_Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse(
        "masters/product_form.html",
        {"request": request, "product": product, "action": "edit"}
    )

@router.post("/products/{product_id}/edit")
async def product_update(
    request: Request,
    product_id: int,
    product_name: str = Form(...),
    product_code: str = Form(None),
    lender_id: int = Form(None),
    interest_rate: float = Form(None),
    min_loan_amount: float = Form(None),
    max_loan_amount: float = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.product import update_product, ProductUpdate
    product_data = ProductUpdate(
        product_name=product_name,
        product_code=product_code,
        lender_id=lender_id,
        interest_rate=interest_rate,
        min_loan_amount=min_loan_amount,
        max_loan_amount=max_loan_amount
    )
    update_product(product_id, product_data, db)
    return RedirectResponse(url="/masters/products", status_code=303)

@router.get("/products/{product_id}/delete")
async def product_delete(product_id: int, db: Session = Depends(get_db)):
    from src.masters.api.product import delete_product
    delete_product(product_id, db)
    return RedirectResponse(url="/masters/products", status_code=303)

# EMPLOYEE UI ROUTES
@router.get("/employees")
async def employee_list(request: Request, db: Session = Depends(get_db)):
    employees = db.query(MST_Employee).filter(MST_Employee.is_active == True).all()
    return templates.TemplateResponse(
        "masters/employee_list.html",
        {"request": request, "employees": employees}
    )

@router.get("/employees/add")
async def employee_add_form(request: Request):
    return templates.TemplateResponse(
        "masters/employee_form.html",
        {"request": request, "employee": None, "action": "add"}
    )

@router.post("/employees")
async def employee_create(
    request: Request,
    employee_code: str = Form(...),
    full_name: str = Form(...),
    designation: str = Form(None),
    department: str = Form(None),
    branch_id: int = Form(None),
    email: str = Form(None),
    mobile: str = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.employee import create_employee, EmployeeCreate
    employee_data = EmployeeCreate(
        employee_code=employee_code,
        full_name=full_name,
        designation=designation,
        department=department,
        branch_id=branch_id,
        email=email,
        mobile=mobile
    )
    create_employee(employee_data, db)
    return RedirectResponse(url="/masters/employees", status_code=303)

@router.get("/employees/{employee_id}/edit")
async def employee_edit_form(request: Request, employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(MST_Employee).filter(MST_Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return templates.TemplateResponse(
        "masters/employee_form.html",
        {"request": request, "employee": employee, "action": "edit"}
    )

@router.post("/employees/{employee_id}/edit")
async def employee_update(
    request: Request,
    employee_id: int,
    employee_code: str = Form(...),
    full_name: str = Form(...),
    designation: str = Form(None),
    department: str = Form(None),
    branch_id: int = Form(None),
    email: str = Form(None),
    mobile: str = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.employee import update_employee, EmployeeUpdate
    employee_data = EmployeeUpdate(
        employee_code=employee_code,
        full_name=full_name,
        designation=designation,
        department=department,
        branch_id=branch_id,
        email=email,
        mobile=mobile
    )
    update_employee(employee_id, employee_data, db)
    return RedirectResponse(url="/masters/employees", status_code=303)

@router.get("/employees/{employee_id}/delete")
async def employee_delete(employee_id: int, db: Session = Depends(get_db)):
    from src.masters.api.employee import delete_employee
    delete_employee(employee_id, db)
    return RedirectResponse(url="/masters/employees", status_code=303)

# CONNECTOR UI ROUTES
@router.get("/connectors")
async def connector_list(request: Request, db: Session = Depends(get_db)):
    connectors = db.query(MST_Connector).filter(MST_Connector.is_active == True).all()
    return templates.TemplateResponse(
        "masters/connector_list.html",
        {"request": request, "connectors": connectors}
    )

@router.get("/connectors/add")
async def connector_add_form(request: Request):
    return templates.TemplateResponse(
        "masters/connector_form.html",
        {"request": request, "connector": None, "action": "add"}
    )

@router.post("/connectors")
async def connector_create(
    request: Request,
    connector_code: str = Form(...),
    full_name: str = Form(...),
    pan: str = Form(None),
    gstin: str = Form(None),
    bank_name: str = Form(None),
    account_number: str = Form(None),
    ifsc: str = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.connector import create_connector, ConnectorCreate
    connector_data = ConnectorCreate(
        connector_code=connector_code,
        full_name=full_name,
        pan=pan,
        gstin=gstin,
        bank_name=bank_name,
        account_number=account_number,
        ifsc=ifsc
    )
    create_connector(connector_data, db)
    return RedirectResponse(url="/masters/connectors", status_code=303)

@router.get("/connectors/{connector_id}/edit")
async def connector_edit_form(request: Request, connector_id: int, db: Session = Depends(get_db)):
    connector = db.query(MST_Connector).filter(MST_Connector.connector_id == connector_id).first()
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    return templates.TemplateResponse(
        "masters/connector_form.html",
        {"request": request, "connector": connector, "action": "edit"}
    )

@router.post("/connectors/{connector_id}/edit")
async def connector_update(
    request: Request,
    connector_id: int,
    connector_code: str = Form(...),
    full_name: str = Form(...),
    pan: str = Form(None),
    gstin: str = Form(None),
    bank_name: str = Form(None),
    account_number: str = Form(None),
    ifsc: str = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.connector import update_connector, ConnectorUpdate
    connector_data = ConnectorUpdate(
        connector_code=connector_code,
        full_name=full_name,
        pan=pan,
        gstin=gstin,
        bank_name=bank_name,
        account_number=account_number,
        ifsc=ifsc
    )
    update_connector(connector_id, connector_data, db)
    return RedirectResponse(url="/masters/connectors", status_code=303)

@router.get("/connectors/{connector_id}/delete")
async def connector_delete(connector_id: int, db: Session = Depends(get_db)):
    from src.masters.api.connector import delete_connector
    delete_connector(connector_id, db)
    return RedirectResponse(url="/masters/connectors", status_code=303)
