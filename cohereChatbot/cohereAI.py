"""
Buiding a chatbot using cohere's API and langchain
"""
import getpass
import os
from langchain_core.messages import HumanMessage
from .cohereAPI import API
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_cohere import ChatCohere


os.environ["COHERE_API_KEY"] = API


model = ChatCohere(model="command-r")

model.invoke([HumanMessage(content="Hi! I'm Bob")])

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    get_session_history: function to get specific conversation history
                        based on the provided session_id
    Args:
        session_id: specific id for histry retrival
    return: the message history
    """
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def invoke_model(query: str, user_id: str):
    """
    invoke_model: uses cohere's API to invoke an AI "Coral"
    Args:
        query: set of questions the user askes
        user_id: unique id of the user for message history
    """
    with_message_history = RunnableWithMessageHistory(model, get_session_history)
    config = {"configurable": {"session_id": user_id}}
    response = with_message_history.invoke(
        [HumanMessage(content=query)],
        config=config,
         )
    return response
    
""" FOR STREAMING PURPOSE
    for r in with_message_history.stream(
        [HumanMessage(content=query)],
        config=config,
         ):
        print(r.content, end="")
"""
