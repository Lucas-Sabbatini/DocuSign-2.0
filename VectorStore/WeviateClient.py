import weaviate
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from .WeaviateCollection import WeaviateCollection


class WeaviateClient:
    @staticmethod
    def connect():
        weaviate_client = weaviate.connect_to_local()
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        return weaviate_client, embeddings
    
    @staticmethod
    def addDocuments(docs: list[Document]) -> list[str]:
        client, embeddings = WeaviateClient.connect()
        collection = WeaviateCollection.getCollection(client=client)
        ids = []
        try:
            with collection.batch.dynamic() as batch:
                for i, d in enumerate(docs):
                    # Gerar embeddings com o OpenAI
                    response = embeddings.embed_query(d.page_content)
                    # Adiciona o objeto com o texto e o embedding e captura o ID retornado
                    obj_id = batch.add_object(
                        properties={"text": d.page_content},
                        vector=response,
                    )
                    print(f"Objeto adicionado \n ID: {obj_id} Progresso: {(i+1)/len(docs)*100}")
                    ids.append(obj_id)
            return ids
        finally:
            client.close()

    @staticmethod
    def searchOnStore(query: str) -> list[Document]:
        client, embeddings = WeaviateClient.connect()
        collection = WeaviateCollection.getCollection(client=client)
        try:
            # Gera o embedding da query
            query_embedding = embeddings.embed_query(query)
            # Executa a query com base no embedding
            result = collection.query.near_vector(near_vector=query_embedding, limit=1)
            # Supondo que o resultado possua uma lista de objetos no atributo "objects"
            documents = []
            for obj in result.objects:
                # Recupera o conteúdo e os metadados do objeto retornado
                properties = obj.properties
                text = properties.get("text", "")
                # Remova a chave "text" dos metadados para evitar duplicidade, se desejar
                metadata = {k: v for k, v in properties.items() if k != "text"}
                documents.append(Document(page_content=text, metadata=metadata))
            return documents
        finally:
            client.close()

        



if __name__ == '__main__':
    print(WeaviateClient.searchOnStore("Teste"))