from fastapi import APIRouter, Depends, status, HTTPException


router = APIRouter(
    tags=["authentication"],
    prefix="/auth"
)

@router.post("/login")
def login():
    return {"message": "Login successful"}