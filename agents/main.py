from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.schema import SystemMessage  # in order to add further info for context
from dotenv import load_dotenv

# calling our tool
from tools.sql import run_query_tool, list_tables

load_dotenv()

chat = ChatOpenAI()
tables = list_tables()

prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(
            content=f"You are an AI that has access to a SQLite database.\n{tables}"
        ),
        # takes in input variable
        HumanMessagePromptTemplate.from_template("{input}"),
        # looks for input var with given name, finds data assigned to name, and explodes with greater number of messages
        MessagesPlaceholder(
            variable_name="agent_scratchpad"  # agent_scratchpad is simplified form of memory to remember conversations
        ),
    ]
)

tools = [run_query_tool]

agent = OpenAIFunctionsAgent(llm=chat, prompt=prompt, tools=tools)

agent_executor = AgentExecutor(agent=agent, verbose=True, tools=tools)

agent_executor("How many users have a shipping address?")
