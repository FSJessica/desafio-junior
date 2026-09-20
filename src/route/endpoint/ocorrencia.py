# endpoints HTTP (fino: só valida e orquestra)

from flask import Blueprint, request
from pydantic import ValidationError

from src.client.cep_client import CepConsultaError
from src.manager import ocorrencia_manager
from src.model.schema.ocorrencia import OcorrenciaInputSchema
from src.utils import json_response

ocorrencia_bp = Blueprint("ocorrencia", __name__)

@ocorrencia_bp.route("/ocorrencia", methods=["POST"])
def criar_ocorrencia():
    try:
        dados = OcorrenciaInputSchema(**request.get_json())
    except ValidationError as erro:
        return json_response.error(str(erro), status=400)

    try:
        ocorrencia = ocorrencia_manager.criar_ocorrencia(dados)
    except CepConsultaError as erro:
        return json_response.error(str(erro), status=400)

    return json_response.success(ocorrencia, status=201)

@ocorrencia_bp.route("/ocorrencia/<placa>", methods=["GET"])
def listar_ocorrencias(placa):
    ocorrencias = ocorrencia_manager.listar_ocorrencias(placa)
    return json_response.success(ocorrencias, status=200)