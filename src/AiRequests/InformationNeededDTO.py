import json
from dataclasses import dataclass
from typing import List

@dataclass
class InformationNeededDTO:
    legislacoes: List[str]

    @staticmethod
    def parseJsonToClass(json_str: str):
        # Converte a string JSON para um dicionário Python
        data = json.loads(json_str)
        # Instancia a classe utilizando desempacotamento de dicionário
        return InformationNeededDTO(**data)


if __name__ == '__main__':
    json_str = '''
    {
    "legislacoes": [
        "Código Civil",
        "Lei do Inquilinato",
        "Código Florestal",
        "Normas do INCRA",
        "Normas da ANVISA"
    ]
    }
    '''
    info = InformationNeededDTO.parseJsonToClass(json_str)
    print(info)
