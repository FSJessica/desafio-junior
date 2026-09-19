# "banco de dados" em memória (ver seção abaixo)

_ocorrencias: list[dict] = []

def inserir(ocorrencia: dict) -> None:
    _ocorrencias.append(ocorrencia)

def listar_por_placa(placa: str) -> list[dict]:
    return [ocorrencia for ocorrencia in _ocorrencias if ocorrencia["placa"] == placa]