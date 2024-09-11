from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from app import models, schemas, security, file_utils
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
import aiofiles

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = security.decode_token(token)
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

@router.post("/users/", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = security.create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/files/upload/")
async def upload_file(file: UploadFile, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    encrypted_content = file_utils.encrypt_file(await file.read())
    db_file = models.File(owner_id=current_user.id, filename=file.filename, data=encrypted_content)
    db.add(db_file)
    db.commit()
    return {"filename": file.filename}

@router.get("/files/download/{file_id}")
async def download_file(file_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_file = db.query(models.File).filter(models.File.id == file_id, models.File.owner_id == current_user.id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    decrypted_content = file_utils.decrypt_file(db_file.data)
    return {"filename": db_file.filename, "content": decrypted_content}

@router.delete("/files/delete/{file_id}")
def delete_file(file_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_file = db.query(models.File).filter(models.File.id == file_id, models.File.owner_id == current_user.id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    db.delete(db_file)
    db.commit()
    return {"message": "File deleted"}
