from langchain_openai import ChatOpenAI
from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

# Initialize the chat model
chat = ChatOpenAI()

# Create a prompt template
prompt = ChatPromptTemplate(
    input_variables=["content"],  # Only content as input, history is handled separately
    messages=[
        MessagesPlaceholder(variable_name="history"),  # Placeholder for conversation history
        HumanMessagePromptTemplate.from_template("{content}")
    ]
)

# Build the base chain (without memory)
chain = prompt | chat

# Create a single chat history instance
chat_history = FileChatMessageHistory("messages.json")

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Return the chat history (ignoring session_id for simplicity)."""
    return chat_history

# Wrap the chain with message history handling
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="content",
    history_messages_key="history",
)

# Main conversation loop
while True:
    content = input(">> ")
    
    # Exit condition
    if content.lower() in ['exit', 'quit']:
        print("Goodbye!")
        break
    
    # Run the chain with automatic history management
    result = chain_with_history.invoke(
        {"content": content},
        config={"configurable": {"session_id": "default"}}  # Required by RunnableWithMessageHistory API
    )
    
    print(result.content)