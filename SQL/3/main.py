from fastapi import FastAPI
from pydantic import BaseModel


class CreateAccountRequest(BaseModel):
    owner: str
    initial_balance: float = 0.0


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


# Временное хранилище
fake_db = {}
next_id = 1


@app.post("/accounts")
def create_account(request: CreateAccountRequest):
    global next_id
    account = {
        "id": next_id,
        "owner": request.owner,
        "balance": request.initial_balance
    }
    fake_db[next_id] = account
    next_id += 1
    return account


@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    if account_id not in fake_db:
        return {"error": "Account not found"}
    return fake_db[account_id]


@app.put("/accounts/{account_id}")
def update_account(account_id: int, balance: float):
    if account_id not in fake_db:
        return {"error": "Account not found"}
    fake_db[account_id]["balance"] = balance
    return fake_db[account_id]


@app.delete("/accounts/{account_id}")
def delete_account(account_id: int):
    if account_id not in fake_db:
        return {"error": "Account not found"}
    del fake_db[account_id]
    return {"message": "Account deleted"}
