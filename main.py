import os
import streamlit as st
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from openai import OpenAI
from joblib import dump, load
import openai

# Load OpenAI API key from .config file
def load_api_key():
    try:
        with open(".config", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        st.error("OpenAI API key not found. Please add it to the .config file.")
        return None

# Save FAISS index
def save_faiss_index(vectorstore, filename="faiss_store_openai.pkl"):
    dump(vectorstore, filename)

# Load FAISS index
def load_faiss_index(filename="faiss_store_openai.pkl"):
    try:
        return load(filename)
    except FileNotFoundError:
        return None

# Query OpenAI for answers
def query_openai(prompt, api_key, model="text-davinci-003"):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=1000  # Ensure the response fits within token limits
    )
    return response.choices[0].text.strip()

# Sidebar input
st.sidebar.header("Scheme Research Tool")
urls = st.sidebar.text_area("Enter URLs (one per line):", height=200)
process_button = st.sidebar.button("Process URLs")

# Main content
st.title("Automated Scheme Research Tool")
st.write("Upload URLs to fetch, process, and query scheme data.")

if process_button:
    api_key = load_api_key()
    if not api_key:
        st.stop()

    openai_embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    url_list = urls.strip().split("\n")
    if not url_list:
        st.error("Please enter at least one URL.")
        st.stop()

    # Load content from URLs
    st.info("Fetching and processing content from URLs...")
    documents = []
    for url in url_list:
        try:
            loader = UnstructuredURLLoader(urls=[url])
            raw_documents = loader.load()
            
            # Preprocessing to extract relevant text
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)
            split_docs = text_splitter.split_documents(raw_documents)
            documents.extend(split_docs)
        except Exception as e:
            st.error(f"Failed to load content from {url}: {e}")

    if not documents:
        st.error("No content loaded from the provided URLs.")
        st.stop()

    # Create embeddings and FAISS index
    st.info("Generating embeddings and creating FAISS index...")
    vectorstore = FAISS.from_documents(documents, openai_embeddings)
    save_faiss_index(vectorstore)

    st.success("Processing complete! FAISS index created and saved.")

# Query section
st.header("Query the Schemes")
query = st.text_input("Enter your question:")
query_button = st.button("Get Answer")

if query_button:
    vectorstore = load_faiss_index()
    if not vectorstore:
        st.error("FAISS index not found. Please process URLs first.")
        st.stop()

    st.info("Fetching answer...")
    try:
        # Perform similarity search
        docs = vectorstore.similarity_search(query, k=5)  # Retrieve top 5 chunks
        relevant_text = " ".join([doc.page_content for doc in docs])
        
        # Query OpenAI with the relevant chunks
        prompt = f"The following is relevant information:\n{relevant_text}\n\nAnswer the question: {query}"
        answer = query_openai(prompt, api_key)

        st.write(f"**Answer:** {answer}")
        for doc in docs:
            st.write(f"**Source URL:** {doc.metadata.get('source', 'Unknown')}")
            st.write(f"**Relevant Content:** {doc.page_content}")
    except Exception as e:
        st.error(f"Failed to retrieve answer: {e}")


