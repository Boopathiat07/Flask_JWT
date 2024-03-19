from pydantic import BaseModel, constr, EmailStr

class Signup(BaseModel):
    name: constr(strip_whitespace=True,max_length=50)
    email: EmailStr
    mobile: constr(strip_whitespace=True,max_length=10, min_length=10)
    password : str

class Login(BaseModel):
    email: EmailStr
    password : str