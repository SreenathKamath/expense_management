from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
import jwt
from sqlalchemy.exc import IntegrityError #while hitting the integrity constrains from DB 
from fastapi.security import OAuth2PasswordBearer
import datetime
import json
from models import Expense
from config import Settings

#app starts here
app = FastAPI()
base = declarative_base()

jwt_secret_key = "Settings.jwt_secret_key" 
algorithm = "HS256"
access_token_expires_minutes = 30
OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")
@jwt_required
def verify_jet(str):
    try:
        payload = jwt.encode(str, jwt_secret_key, algorithm=algorithm)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

#db connection- suppose it is a postgres
db_username = "Settings.DB_USERNAME"
db_password = "Settings.DB_PASSWORD"
db_host = "Settings.DB_HOST"
get_db_url = f"postgresql://{db_username}:{db_password}@{db_host}/dbname"
engine= create_engine(get_db_url)

#Insert into Expense table, suppose it is a json context passing with the input params with jwt security
@app.post("/api/expenses/")
@jwt_required
async def add_expense(body:dict,db=engine):
    context = body
    name = context.get("name")
    amount = context.get("amount")
    category = context.get("category")
    new_expense_data = Expense(name=name, amount=amount, category=category)
    try:
        await db.commit(new_expense_data)
    except IntegnityError as e:
        await db.rollback()
        return {"error": "Failed to add expense", "details": str(e)}    
    return {"message": "Expense added successfully", "expense": new_expense_data.__dict__}    

# get the inserted data from the table with jwt security
@app.get("/api/expenses/")
@jwt_required
async def get_expenses(db_engine=engine):
    try:
        expenses = await db_engine.query(Expense).all()
        return {"expenses": [expense.__dict__ for expense in expenses]}
    except Exception as e:
        return {"error": "Failed to retrieve expenses", "details": str(e)}


#get the expense data according to the Filter Expenses by Month, Week, Day, Category API
@app.get("/api/expenses/month/{year}/{month}/")
async def get_expense_byyear_month(year:int,month:int,db_engine=engine):
    try:
        expenses = await db_engine.query(Expense).filter(Expense.year == year, Expense.month == month).all()
        expense = json.loads(json.dumps([expense.__dict__ for expense in expenses], default=str))
        return {"expenses": expense}
    except Exception as e:
        return {"error": "Failed to retrieve expenses", "details": str(e)}

# Implement an API endpoint to retrieve total expenses, total salary, and remaining amount.
@app.get("/api/expenses/summary/")
async def total_expense_summary(db_engine=engine):
    try:
        total_expenses = await db_engine.query(func.sum(Expense.amount)).scalar()
        total_salary = 5000  # Assuming a fixed salary for demonstration
        remaining_amount = total_salary - total_expenses
        return {
            "total_expenses": total_expenses,
            "total_salary": total_salary,
            "remaining_amount": remaining_amount
        }
    except Exception as e:
        return {"error": "Failed to retrieve expense summary", "details": str(e)}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0", port=8000)