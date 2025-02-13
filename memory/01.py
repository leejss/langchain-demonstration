from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def demonstrate_basic_memory():
    """
    Demonstrates basic usage of ConversationBufferMemory
    """
    # Initialize memory
    memory = ConversationBufferMemory()

    # Save some context to memory
    memory.save_context(
        {"human": "Hi, my name is John."}, {"ai": "Hello John! Nice to meet you."}
    )

    # Retrieve memory variables
    print("Basic Memory Retrieval:")

    # {'history': 'Human: Hi, my name is John.\nAI: Hello John! Nice to meet you.'}
    print(memory.load_memory_variables({}))
    print("\n")


def demonstrate_conversation_chain():
    """
    ConversationBufferMemory with LLM Chain
    """

    llm = ChatOpenAI(temperature=0)
    memory = ConversationBufferMemory()

    # conversation chain
    conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

    response1 = conversation.predict(
        input="Hi, my name is John. I'm planning a trip to New York."
    )
    print("Response 1:", response1)

    response2 = conversation.predict(input="What was my name again?")
    print("Response 2:", response2)

    # Show memory variables
    print("Memory Variables:")
    print(memory.load_memory_variables({}))


if __name__ == "__main__":
    # demonstrate_basic_memory()
    demonstrate_conversation_chain()
