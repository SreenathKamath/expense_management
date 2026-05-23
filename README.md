The Expense Management website is used for storing the expenses of the user, we have the features to input the expense data with POST /api/expense/ api, then we can see the inserted one's by GET /api/expense api, then the totla by /api/expenses/summary/ GET api, then monthly of a user using GET /api/expenses/month/{year}/{month}/ api.

we are using the postgresql table name 'expense' for the DB side

Secured by jwt tokens so not much bombarding to the api's by the public wthout the access.

all tamper proof variables are stored in .env folder

ORM model in models.py

Pydantic base settings in config.py
