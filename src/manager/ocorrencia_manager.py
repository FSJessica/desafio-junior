# regra de negócio / orquestração

import uuid

from src.client.cep_client import consultar_cep, CepConsultaError
from src.model import repository
from src.model.schema.ocorrencia import OcorrenciaInputSchema

def criar_ocorrencia(dados: OcorrenciaInputSchema) -> dict:
    endereco = consultar_cep(dados.cep)

    ocorrencia = {
        "id": str(uuid.uuid4()),
        "placa": dados.placa,
        "tipo": dados.tipo,
        "descricao": dados.descricao,
        "dataOcorrencia": dados.dataOcorrencia.isoformat(),
        "endereco": {
            "logradouro": endereco.get("logradouro"),
            "bairro": endereco.get("bairro"),
            "localidade": endereco.get("localidade"),
            "uf": endereco.get("uf"),
        },
    }

    repository.inserir(ocorrencia)

    return ocorrencia

def listar_ocorrencias(placa: str) -> list[dict]:
    return repository.listar_por_placa(placa)

def deletar_ocorrencia(ocorrencia_id: str) -> bool:
    return repository.remover_por_id(ocorrencia_id)