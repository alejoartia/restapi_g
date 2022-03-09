# libraries 
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from .redis import limiter

# resources 
import app.src.federacion_scrap as _federacion_scrap
import app.src.fixer_api as _fixer_api
import app.src.banxico_api as _banxico_api
import app.config as cfg

items_federacion = _federacion_scrap.convert_to_dict()
items_fixer = _fixer_api.currency_of_the_day()
items_banxico = _banxico_api.currency_of_the_day()
message = cfg.MESSAGE

fake_users_db = {
    "alejo": {
        "username": "alejo",
        "full_name": "alejo cordoba",
        "email": "jalejo@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "juliet": {
        "username": "juliet",
        "full_name": "juliet mar",
        "email": "juliet@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

#limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
#app.state.limiter = limiter
#app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/rates")
async def read_item(token: str = Depends(oauth2_scheme)):

    clientIp = request.client.host
    res = limiter(clientIp, 5)

    if res["call"]:
        return {'rates':
        {'federacion':items_federacion,
        'fixer': items_fixer,
        'banxio': items_banxico
        }}

    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,      
            detail={
                "message": "call limit reached",
                "ttl": res["ttl"]
                })


# go here to see a wonder message 
@app.get("/message")
async def read_item():

    clientIp = request.client.host
    res = limiter(clientIp, 5)

    if res["call"]:
        return {"remember": message}
    
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,      
            detail={
                "message": "call limit reached",
                "ttl": res["ttl"]
                })