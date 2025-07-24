# Basics of LangChain

### 1. Create prompt template
    prompt = PromptTemplate(
    template="Write about {topic}",
    input_variables=["topic"]
    )

### 2. Create chain (simple)
    chain = prompt | llm

### 3. Run chain (ALWAYS use dictionary!)
    result = chain.invoke({"topic": "cats"})

# Sequential Chain
    def create_chain():
        chain_1 = prompt_1 | llm
        chain_2 = (
        {"key1: RunnablePassthrough(), key_2: chain"} | prompt_2 | llm
        )
        return chain_2

    result = chain_2.invoke({"key1": args.name})

# Calling the LLM
    llm = OpenAI() 
    # this is older, completion model

    llm = ChatOpenAI()
    # newer chat conversational model

# Chains
### Old way (not needed anymore)
    chain = LLMChain(llm=chat, prompt=prompt)
### new LangChain syntax
    chain = prompt | chat
    # this creates RunnableSequence internally to handle a chain
    # input goes to prompt first --> prompt formats input with template --> formatted prompt goes to chat mode --> chat model generates response


