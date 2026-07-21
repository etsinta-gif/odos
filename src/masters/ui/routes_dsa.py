from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from src.core.database import get_db
from src.masters.api.dsa import create_dsa, delete_dsa, get_dsa, list_dsas, update_dsa, DSACreate, DSAUpdate
from src.security.auth import get_current_user

router = APIRouter(prefix="/masters/dsas", tags=["Masters UI"], dependencies=[Depends(get_current_user)])

templates = Jinja2Templates(directory="src/templates")


@router.get("")
@router.get("/")
def dsa_list(request: Request, search: str | None = None, db=Depends(get_db)):
    dsas = list_dsas(skip=0, limit=500, search=search, db=db)
    return templates.TemplateResponse(
        "masters/dsa_list.html",
        {
            "request": request,
            "dsas": dsas,
            "search": search or "",
        },
    )


@router.get("/add")
def dsa_add_form(request: Request):
    return templates.TemplateResponse(
        "masters/dsa_form.html",
        {
            "request": request,
            "dsa": None,
            "action": "add",
        },
    )


@router.post("")
def dsa_create(
    dsa_code: str = Form(...),
    dsa_name: str = Form(...),
    contact_person: str | None = Form(None),
    email: str | None = Form(None),
    mobile: str | None = Form(None),
    db=Depends(get_db),
):
    dsa_data = DSACreate(
        dsa_code=dsa_code,
        dsa_name=dsa_name,
        contact_person=contact_person,
        email=email,
        mobile=mobile,
        is_active=True,
    )
    dsa = create_dsa(dsa_data, db)
    return RedirectResponse(url=f"/masters/dsas/{dsa.dsa_id}/edit", status_code=303)


@router.get("/{dsa_id}")
def dsa_detail(request: Request, dsa_id: int, db=Depends(get_db)):
    dsa = get_dsa(dsa_id, db)
    return templates.TemplateResponse(
        "masters/dsa_form.html",
        {
            "request": request,
            "dsa": dsa,
            "action": "edit",
        },
    )


@router.get("/{dsa_id}/edit")
def dsa_edit_form(request: Request, dsa_id: int, db=Depends(get_db)):
    dsa = get_dsa(dsa_id, db)
    return templates.TemplateResponse(
        "masters/dsa_form.html",
        {
            "request": request,
            "dsa": dsa,
            "action": "edit",
        },
    )


@router.post("/{dsa_id}/edit")
def dsa_update(
    dsa_id: int,
    dsa_code: str = Form(...),
    dsa_name: str = Form(...),
    contact_person: str | None = Form(None),
    email: str | None = Form(None),
    mobile: str | None = Form(None),
    db=Depends(get_db),
):
    dsa_data = DSAUpdate(
        dsa_code=dsa_code,
        dsa_name=dsa_name,
        contact_person=contact_person,
        email=email,
        mobile=mobile,
        is_active=True,
    )
    update_dsa(dsa_id, dsa_data, db)
    return RedirectResponse(url=f"/masters/dsas/{dsa_id}/edit", status_code=303)


@router.get("/{dsa_id}/delete")
def dsa_delete(dsa_id: int, db=Depends(get_db)):
    delete_dsa(dsa_id, db)
    return RedirectResponse(url="/masters/dsas", status_code=303)
