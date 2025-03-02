from AiRequests.AiRequest import AiRequest
from VectorStore.WeviateClient import WeaviateClient

print(
    "Bem vindo ao DocuSign 2.0, por favor digite um prompt para contrato ou documento"
)
prompt = input()

aiRequest = AiRequest()
itemsToSearch = aiRequest.getInformationNeeded(prompt)

vectorStoreResponses = []
for itemToSearch in itemsToSearch:
    vectoreStoreResponse = WeaviateClient.searchOnStore(itemToSearch)
    vectorStoreResponses.append(vectoreStoreResponse[0].page_content)

response = aiRequest.getContract(
    prompt=prompt, informationNeeded=itemsToSearch, storeRetrivals=vectorStoreResponses
)
print(response)
