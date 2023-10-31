from datetime import datetime, timedelta
from jose import JWTError, jwt
import schemas
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException



SECRET_KEY = "d2681ae06fc0d4098dfd7502b5f815692d31afcd6722608c3d604dd66f244167"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()  # just don't want to change the real data 
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)  # token is made
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try : 
        #print("token at verify_access_token", token)
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        #print("decoded successfully") 
        id : int|None = payload.get("user_id")
        #print(type(id))
        if id == None : raise credential_exception 
        token_data = schemas.tokenData(id=id) 
    except JWTError:
        raise credential_exception 
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)): 
    print("token at get_current_user:", token, oauth2_scheme)
    credential_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail=f"Could not validate credentials", 
                headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credential_exception)
    
    
    