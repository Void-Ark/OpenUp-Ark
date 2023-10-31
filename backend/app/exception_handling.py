from fastapi import status, HTTPException


def credential_exception(Exception):
        return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail=f"Could not validate credentials", 
                headers={"WWW-Authenticate": "Bearer"})
