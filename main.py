# run pipenv shell to load enviromment, then python main.py
# updated imports from video because that was deprecated
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import argparse
from dotenv import load_dotenv
import os

# set up env file and set up parsing arguments
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--name", default="Superman")
args = parser.parse_args()

# automatically looks for api key in .env file
llm = OpenAI()

# create prompt template
prompt_1 = PromptTemplate(
    # must declare prompt and variables
    template= "Write a sentence about {superhero}'s powers",
    input_variables = ["superhero"]
)

prompt_2 = PromptTemplate(
    # must declare prompt and variables
   template="Here is a sentence about {superhero}'s powers: '{text}'\nWrite another sentence about a superhero with similar powers",
   input_variables=["superhero", "text"]
)

# LangChain Expression for chaining sequentially
def create_sequential_chain():
    # basic chain
    chain_1 = prompt_1 | llm

    sequential_chain = (
        {"superhero": RunnablePassthrough(), "text": chain_1} | prompt_2 | llm
    )
    return sequential_chain


chain = create_sequential_chain()
result = chain.invoke({"superhero": args.name})

print(result)