# establish connection to db file
import sqlite3

from langchain.tools import Tool
from pydantic.v1 import BaseModel
from typing import List

conn = sqlite3.connect("db.sqlite")


def list_tables():
    c = conn.cursor()
    c.execute("SELECT name from sqlite_master WHERE type = 'table';")
    rows = c.fetchall()  # retrieves all rows returned by the query
    return "\n".join(row[0] for row in rows if row[0] is not None)


# take SQL query string as input and execute the query and return
def run_sqlite_query(query):
    c = conn.cursor()  # allows us to access database
    try:
        c.execute(query)
        return c.fetchall()  # return all information as result of query
    except sqlite3.OperationalError as err:
        return f"The following error occured: {str(err)}"


# basically just better describes arguments to ChatGPT
class RunQueryArgsSchema(BaseModel):
    query: str


# wraps query function as a LangChain tool
run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a SQLite query.",
    func=run_sqlite_query,
    args__schema=RunQueryArgsSchema,
)


def describe_tables(table_names):
    c = conn.cursor()
    result = []
    for table in table_names:
        result.append("'" + table + "'")
    tables = ", ".join(result)
    rows = c.execute(
        f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});"
    )
    return "\n".join(row[0] for row in rows if row[0] is not None)


# just getting more information; kinda understand it but a little in the weeds
class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]


describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, return the schema of those tables",
    func=describe_tables,
)
