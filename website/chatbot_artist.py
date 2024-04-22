import os
from PyPDF2 import PdfFileReader
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import TextSplitter
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

text_splitter = CharacterTextSplitter()

llm = ChatOpenAI()

class PDFLoader:
    def __init__(self, artist):
        self.artist = artist
    
    def load_and_split(self):
        documents = []
        directory = '../Wikipedia/pdfs/'
        with open(os.path.join(directory, f'{self.artist}.pdf'), 'rb') as f:
            pdf = PdfFileReader(f)
            text = ''
            text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
            documents.extend(text_splitter.split(text))
        return documents


# 필요 X -> 추후 지우기
pdf_directory = '../Wikipedia/pdfs/Vincent_van_Gogh'

# Define the cache directory
cache_dir = LocalFileStore('./cache')

# Define the text splitter
splitter = CharacterTextSplitter.from_tiktoken_encoder(
    separator="\n",
    chunk_size=500,
    chunk_overlap=100,
)

pdf_loader = PDFLoader('Vincent_van_Gogh')

# Load and split the documents
docs = pdf_loader.load_and_split(text_splitter=splitter)

# Embeddgins and cache
embeddings = OpenAIEmbeddings()
cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)

# Vector Store and retrieval
vector_store = FAISS.from_embeddings(docs, cached_embeddings)
retriever = vector_store.as_retriever()

# prompt template
prompt = ChatPromptTemplate(
    [
         (
            "system",
            """
            You are a chatbot that knows a lot about Vincent van Gogh. You can answer any questions about him.
            \n\n
            {context}",
            """
        ),
        ("human", "{question}"),
    ]
)

chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
)

result = chain.invoke("What is the most famous painting of Vincent van Gogh?")
print(result)