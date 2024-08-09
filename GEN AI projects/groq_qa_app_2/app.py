import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

st.title("Indian Budget QA chatbot")
def build_retriever():
    docs = PyPDFDirectoryLoader("./data").load()
    print("len of data:", len(docs))
    if not docs:
        raise ValueError("No documents were loaded. Please check the data directory.")
    chunks = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200).split_documents(docs)
    print("len of chunks:",len(chunks))

    # select embeddings 
    # embeddings = OllamaEmbeddings(model = "nomic-embed-text")
    embeddings = OpenAIEmbeddings()
    
    vectorstore = FAISS.from_documents(chunks ,embeddings)
    print("vector_store_created...")
    retriever = vectorstore.as_retriever()
    return retriever

if st.button("load_documents"):
    if "retriever" not in st.session_state:
        with st.spinner("Loading documents..."):
            retriever = build_retriever()
            st.session_state.retriever = retriever

prompt = ChatPromptTemplate.from_template(
                '''Answer the following question based on provided context only.
                <context>
                {context}
                </context>
                Question: {input}
                '''
            )
llm = ChatGroq(groq_api_key = groq_api_key,
               model_name = 'llama3-8b-8192')
document_chain = create_stuff_documents_chain(llm,prompt)

# Only attempt to create retriever_chain if the retriever has been initialized
if "retriever" in st.session_state:
    retriever_chain = create_retrieval_chain(st.session_state.retriever, document_chain)

question = st.text_input("Enter your question here")
get_resp_btn = st.button("GET RESPONSE")
if question and get_resp_btn:
    if "retriever_chain" in locals():
        with st.spinner("Getting Response..."):
            response = retriever_chain.invoke({"input": question})
            st.write(response["answer"])
            with st.expander("Context Used:"):
                for i, doc in enumerate(response["context"]):
                    st.write(doc.page_content)
                    st.write(".............................")
    else:
        st.warning("Please load the documents first by clicking the 'Load Documents' button.")

    