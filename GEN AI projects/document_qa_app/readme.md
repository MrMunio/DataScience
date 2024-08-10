# Document Q/A Chat App

## Overview

This web application allows users to upload and query documents in various formats. It leverages the Langchain framework, GoogleGenerativeAIEmbeddings for accurate context retrieval, FAISS for vector storage, and GROQ Cloud for fast inference. The app supports DOCX, DOC, PDF, and TXT file uploads and can efficiently scan and load a 30-page file in under 7 seconds. The frontend is built with Streamlit for a smooth user experience.

## Features

- **Document Upload**: Supports uploading PDF, DOCX, DOC, and TXT files.
- **Contextual Querying**: Uses Langchain’s `ChatGroq` model for real-time document retrieval and answering questions.
- **Fast Processing**: Scans and loads a 30-page document in under 7 seconds.
- **Beautiful UI**: Built with Streamlit for an intuitive and interactive user experience.

## Technologies

- **Langchain Framework**: For document processing and chain creation.
- **GoogleGenerativeAIEmbeddings**: For accurate context retrieval.
- **FAISS**: For efficient vector storage and retrieval.
- **GROQ Cloud**: For fast and reliable model inference.
- **Streamlit**: For building the user interface.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MrMunio/DataScience/tree/main/GEN%20AI%20projects/document-qa-chat-app.git
   cd document-qa-chat-app
   ```
