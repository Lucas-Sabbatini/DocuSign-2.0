from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from .InformationNeededDTO import InformationNeededDTO

json_str = """
    {
    "legislacoes": [
    ]
    }
    """


class AiRequest:
    def __init__(self):
        self.llm = ChatOpenAI()

    def getInformationNeeded(self, prompt: str) -> list[str]:
        messages = [
            HumanMessage(
                content=f"{prompt} Para isso quero que você me liste quais legislações você precisa, eu vou pesquisar e lhe fornecer os conteúdos de cada legislação e posteriormente pedir para você redigir esse contrato. Escreva a resposta no formato JSON, exemplo: {json_str}"
            )
        ]
        response = self.llm.invoke(messages)
        return InformationNeededDTO.parseJsonToClass(response.content).legislacoes

    def getContract(
        self, prompt: str, informationNeeded: list[str], storeRetrivals: list[str]
    ) -> str:
        promptContext = ""
        for i in range(0, len(informationNeeded)):
            promptContext = (
                promptContext + f"{informationNeeded[i]}: \n{storeRetrivals[i]}\n"
            )

        messages = [
            HumanMessage(
                content=f"{prompt}. Para isso você pode se basear nas legislações que você tem conhecimento e também as que eu vou lhe fornecer abaixo:\n{promptContext}"
            )
        ]
        return self.llm.invoke(messages)
