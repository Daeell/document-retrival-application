import streamlit as st
import datetime
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from QdrantVectorStore import QdrantVectorStore

qdrant_store = QdrantVectorStore(host="localhost", 
                                 port=6333, 
                                 collection_name="chat_collection", 
                                 vector_size=384)

if 'messages' not in st.session_state:
    st.session_state.messages = []

# i want make chat input display with streamlit
def show_chat():
    st.title('Streamlit Chat')
    nickname = st.sidebar.text_input('Enter your nickname')

    if nickname:
        st.sidebar.text('Joined chat as ' + nickname)

        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

        if prompt:=st.chat_input('Enter your chatting'):
            with st.chat_message('user'):
                st.markdown(prompt)

            data = [
                {
                    'nickname':nickname,
                    'question':prompt,
                    'answer':""
                }
            ]
            qdrant_store.upsert_data(data)
            
            st.session_state.messages.append({"role": "user", "content": prompt})


show_chat()