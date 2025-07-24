from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
# from langchain.chains import LLMChain (don't need this import if we use | to create chains)
from dotenv import load_dotenv
load_dotenv()

# need to get conversational model
chat = ChatOpenAI()

# LangChain template to create prompt for chat based model
prompt = ChatPromptTemplate(
    # expects one input var
    input_variables = ['content'],
    # creates a system message that represents what human would say
    messages = [HumanMessagePromptTemplate.from_template("{content}")]
)

# check notes
chain = prompt | chat

while True:
    content = input(">> ")
    # use new .invoke method to execute chains
    result = chain.invoke({"content": content})
    # result object has content attribute, not ["text"]
    print(result.content)