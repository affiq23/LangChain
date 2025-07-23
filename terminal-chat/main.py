from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
# from langchain.chains import LLMChain (don't need this import if we use | to create chains)
from dotenv import load_dotenv
load_dotenv()

chat = ChatOpenAI()

# LangChain template to create prompt for chat based model
prompt = ChatPromptTemplate(
    # expects one input var
    input_variables = ['content'],
    # creates a system message that represents what human would say
    messages = [HumanMessagePromptTemplate.from_template("{content}")]
)

# Old way (not needed anymore)
# chain = LLMChain(llm=chat, prompt=prompt)

# new LangChain syntax
# this creates RunnableSequence internally to handle a chain
# input goes to prompt first --> prompt formats input with template --> formatted prompt goes to chat mode --> chat model generates response
chain = prompt | chat

while True:
    content = input(">> ")
    # use new .invoke method to execute chains
    result = chain.invoke({"content": content})
    # result object has content attribute, not ["text"]
    print(result.content)