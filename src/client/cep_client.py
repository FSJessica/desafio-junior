# chamada HTTP à API pública de CEP (ex: ViaCEP)

import requests

class CepConsultaError(Exception):
    pass

def consultar_cep(cep: str) -> dict:
    try:
        resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
    except requests.RequestException as erro:
        raise CepConsultaError(f"Erro ao consultar o CEP: {erro}")

    dados = resposta.json()

    if dados.get("erro"):
        raise CepConsultaError(f"CEP {cep} não encontrado")

    return dados