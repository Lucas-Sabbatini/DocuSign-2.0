from AiRequests.AiRequest import AiRequest
from VectorStore.WeviateClient import WeaviateClient
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.responses import HTMLResponse

load_dotenv()
app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    prompt = await websocket.receive_text()

    aiRequest = AiRequest()
    itemsToSearch = aiRequest.getInformationNeeded(prompt)

    vectorStoreResponses = []
    for itemToSearch in itemsToSearch:
        vectoreStoreResponse = WeaviateClient.searchOnStore(itemToSearch)
        vectorStoreResponses.append(vectoreStoreResponse[0].page_content)

    response = aiRequest.getContract(
        prompt=prompt,
        informationNeeded=itemsToSearch,
        storeRetrivals=vectorStoreResponses,
    )
    await websocket.send_json(response)


@app.get("/")
async def getIndexHTML():
    with open("./src/Front-End/index.html", "r", encoding="utf-8") as file:
        content = file.read()

    return HTMLResponse(content=content)
