from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Usamos la clave que vimos en el debug
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
        
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        # Intento por si el sub es el teléfono
        user = db.query(User).filter(User.phone == str(user_id)).first()
        
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="No eres admin")
    return current_user
