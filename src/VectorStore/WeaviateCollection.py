from weaviate.classes.config import Property, DataType
from weaviate.classes.query import Filter
import weaviate


class WeaviateCollection:
    # Create a new data collection
    @staticmethod
    def createColection(client):
        collection = client.collections.create(
            name="docs",  # Name of the data collection
            properties=[
                Property(
                    name="text", data_type=DataType.TEXT
                ),  # Name and data type of the property
                Property(name="element_id", data_type=DataType.TEXT),
                Property(name="parent_id", data_type=DataType.TEXT),
            ],
        )
        return collection

    @staticmethod
    def getCollection(client):
        return client.collections.get("docs")

    @staticmethod
    def clearCollecction(client):
        collection = WeaviateCollection.getCollection(client)
        return collection.data.delete_many(where=Filter.by_property("text").like("*"))


if __name__ == "__main__":
    weaviate_client = weaviate.connect_to_local()
    print("Limpando")
    print(WeaviateCollection.clearCollecction(weaviate_client))
    weaviate_client.close()
