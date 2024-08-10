import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
import time

# load api keys
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")  

# initialize streamlit framework
st.title("Web site chat Bot using mixtral-7B from Groq Cloud")
url = st.text_input("Enter web URL to ask questions about")
load_button = st.button("Load Web Page")
if load_button and url:
    # Display a loading message while processing the data
    with st.spinner("Loading data..."):
        if "retrieval_chain" not in st.session_state:
            # display a message to user that the data loading process is in under process
            st.write("Loading data...")
            embeddings = OllamaEmbeddings(model = "nomic-embed-text")
            loader = WebBaseLoader(url)
            docs = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=200)
            chunks = splitter.split_documents(docs)
            vectordb = FAISS.from_documents(chunks, embeddings)
            llm = ChatGroq(groq_api_key = groq_api_key,
                        model_name = "mixtral-8x7b-32768")
            prompt = ChatPromptTemplate.from_template(
                '''Answer the following question based on provided context only.
                <context>
                {context}
                </context>
                Question: {input}
                '''
            )
            document_chain = create_stuff_documents_chain(llm,prompt)
            retriever = vectordb.as_retriever()
            st.session_state.retrieval_chain = create_retrieval_chain(retriever, document_chain)
            print("retrieval_chain created")

query = st.text_input("provide your question here")
if query:
    try: # to catch error while accessing the groq inference endpoint
        start_time = time.time()
        response = st.session_state.retrieval_chain.invoke({"input": query})
        print(f'response time: {time.time()-start_time} sec')
        st.write(response["answer"])
        with st.expander("Context Used:"):
            for i,doc in enumerate(response["context"]):
                st.write(doc.page_content)
                st.write(".............................")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write("Please try again later.") 
