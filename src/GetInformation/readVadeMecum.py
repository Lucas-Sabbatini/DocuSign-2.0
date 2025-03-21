from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_unstructured import UnstructuredLoader
from ..VectorStore.WeviateClient import WeaviateClient

file_path = "Vade_mecum_2023.pdf"
loader = UnstructuredLoader(file_path)

docs = loader.load()
docs_filtrados = [
    doc
    for doc in docs
    if doc.metadata.get("category") not in ["Title", "UncategorizedText"]
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)
all_splits = text_splitter.split_documents(docs)

print(all_splits[0])
ids = WeaviateClient.addDocuments(docs=all_splits)
