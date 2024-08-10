import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
import shutil
import time
from dotenv import load_dotenv
load_dotenv()

# Ensure the temporary directory exists
TEMP_DIR = "./temp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# load API keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
groq_api_key = os.environ["GROQ_API_KEY"]
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

st.title("Documents Q/A Chat App")

def build_retriever(uploaded_files):
    docs = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(TEMP_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Load documents based on their file type
        if uploaded_file.name.endswith(".pdf"):
            pdf_loader = PyPDFLoader(file_path)
            docs.extend(pdf_loader.load())
        elif uploaded_file.name.endswith(".docx"):
            docx_loader = Docx2txtLoader(file_path)
            docs.extend(docx_loader.load())
        elif uploaded_file.name.endswith(".txt"):
            text_loader = TextLoader(file_path)
            docs.extend(text_loader.load())
        else:
            st.warning(f"Unsupported file type: {uploaded_file.name}")
    
    if not docs:
        raise ValueError("No documents were loaded. Please check the uploaded file(s).")
    
    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
    print("processing chunks of length:", len(chunks))

    # Select embeddings 
    # embeddings = OpenAIEmbeddings()
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    # embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # vector store
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("Vector store created...")
    retriever = vectorstore.as_retriever()

    # Clear the contents of TEMP_DIR after the retriever is created
    shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)

    return retriever

# Use the side panel for file uploads
with st.sidebar:
    uploaded_files = st.file_uploader("Upload PDF/Word file(s)", type=["pdf", "docx","doc","txt"], accept_multiple_files=True)
    if st.button("Load Documents"):
        if uploaded_files:
            if "retriever" not in st.session_state:
                with st.spinner("Loading documents..."):
                    start_time = time.time()
                    retriever = build_retriever(uploaded_files)
                    print(f"elapsed time for documents load: {time.time()-start_time} secs")
                    st.session_state.retriever = retriever
                    st.write("documents loaded successfully!")
        else:
            st.warning("Please upload a PDF or Word document first.")

prompt = ChatPromptTemplate.from_template(
    '''Answer the following question based on provided context only.
    <context>
    {context}
    </context>
    Question: {input}
    '''
)
# select model:
# groq_model="gemma-7b-it"
groq_model="llama3-8b-8192"

llm = ChatGroq(groq_api_key=groq_api_key, model_name=groq_model)
document_chain = create_stuff_documents_chain(llm, prompt)

# Only attempt to create retriever_chain if the retriever has been initialized
if "retriever" in st.session_state:
    retriever_chain = create_retrieval_chain(st.session_state.retriever, document_chain)

question = st.text_input("Enter your question here")
get_resp_btn = st.button("Get Response")

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
