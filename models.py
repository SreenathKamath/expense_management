from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float


#ORM Model for expanses
class Expense(base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    amount= Column(Float)
    category= Column(String, index=True)