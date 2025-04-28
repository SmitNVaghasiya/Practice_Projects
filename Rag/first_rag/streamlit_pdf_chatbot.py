from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
import chardet
import re
import os

def chunk_generator(file):
    # Finds the type of the file
    split = os.path.split(file)
    file_type = split[1].lower()

    # Finding the encoding type for the non pdf files
    if file_type != '.pdf':
        try:
            with open(file, 'rb') as f:
                encoding = chardet.detect(f.read())['encoding']
        except Exception as e:
            raise RuntimeError(f"Error detecting the encoding of {file}: {str(e)}")
    else:
        encoding = None

    # Converting the file into the documents or chunks
    try:
        if file_type == '.pdf':
            document = PyPDFLoader(file).load()
        else:
            document = TextLoader(file, encoding=encoding).load()
    except Exception as e:
        raise RuntimeError(f"Error loading {file}: {str(e)}")

    # Removing any extra 'space' or '-' from page.
    for chunk in document:
        chunk.page_content = re.sub(r'\s+', ' ', chunk.page_content).strip()
        chunk.page_content = re.sub(r'-+', '-', chunk.page_content).strip()

    # Finally converting into small chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return text_splitter.split_documents(document)


def vector_generator(chunked_documents):
    embedding = HuggingFaceEmbeddings()
    vector_store = InMemoryVectorStore.from_documents(
        documents=chunked_documents,
        embedding=embedding
    )
    return vector_store


def chat_module(query, db):
    load_dotenv()
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not found in environment variables.")
    
    llm = ChatGroq(
        model_name="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1000
    )

    prompt_template = """
    You are an AI assistant designed to answer questions based solely on the provided context.
    Do not include information outside the given context. If the context is not relevant to the question,
    state that no relevant information is available. Explain the topic in full detail according to the context given.
    Format the response in a way that is clear and understandable.
    Context: {context}
    Question: {question}
    Answer:
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": prompt}
    )

    result = qa_chain.invoke({"query": query})
    return result['result']


# Streamlit app
st.title("Document Q&A System")

# Initialize session state for chat history if not already present
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display the entire chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

uploaded_file = st.file_uploader('Choose a PDF, MD, or TXT file', type=['pdf', 'md', 'txt'])

if uploaded_file is not None:
    temp_file_path = uploaded_file.name
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        chunked_documents = chunk_generator(temp_file_path)
        db = vector_generator(chunked_documents)
        st.success("File processed successfully!")
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        db = None
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    question = st.chat_input("Ask a question about the document")

    if question and db:
        # Append user question to chat history
        st.session_state.chat_history.append({"role": "user", "content": question})
        # Display user question
        with st.chat_message("user"):
            st.write(question)
        
        try:
            answer = chat_module(question, db)
            # Append assistant answer to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            # Display assistant answer
            with st.chat_message("assistant"):
                st.write(answer)
        except Exception as e:
            st.error(f"Error generating answer: {str(e)}")