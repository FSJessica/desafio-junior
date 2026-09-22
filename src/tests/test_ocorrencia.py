import copy

def test_create_ocorrencia_success(client, ocorrencia_payload):
    """Teste: ocorrência criada com sucesso."""
    response = client.post("/ocorrencia", json=ocorrencia_payload)

    assert response.status_code == 201
    assert response.get_json()["success"] is True
    assert response.get_json()["data"]["placa"] == "ABC1D23"
    assert response.get_json()["data"]["endereco"]["logradouro"] == "Rua Teste"

def test_create_ocorrencia_tipo_invalido(client, ocorrencia_payload):
    """Teste: tipo fora do Literal permitido retorna 400."""
    payload = copy.deepcopy(ocorrencia_payload)
    payload["tipo"] = "ROUBO"

    response = client.post("/ocorrencia", json=payload)

    assert response.status_code == 400
    assert response.get_json()["success"] is False
    assert response.get_json()["message"] == "Input should be 'AVARIA', 'MANUTENCAO' or 'MULTA'"

def test_create_ocorrencia_data_futura(client, ocorrencia_payload):
    """Teste: dataOcorrencia no futuro retorna 400."""
    payload = copy.deepcopy(ocorrencia_payload)
    payload["dataOcorrencia"] = "2099-01-01"

    response = client.post("/ocorrencia", json=payload)

    assert response.status_code == 400
    assert response.get_json()["success"] is False
    assert response.get_json()["message"] == "A data da ocorrência não pode ser no futuro"

def test_create_ocorrencia_cep_invalido(client, ocorrencia_payload):
    """Teste: CEP com menos de 8 dígitos retorna 400."""
    payload = copy.deepcopy(ocorrencia_payload)
    payload["cep"] = "123"

    response = client.post("/ocorrencia", json=payload)

    assert response.status_code == 400
    assert response.get_json()["success"] is False
    assert response.get_json()["message"] == "CEP inválido. Use o formato 99999999 ou 99999-999"

def test_create_ocorrencia_cep_nao_encontrado(client, ocorrencia_payload, monkeypatch):
    """Teste: CEP no formato correto mas não encontrado retorna 400, sem stacktrace."""
    from src.client.cep_client import CepConsultaError

    def fake_consultar_cep_erro(cep):
        raise CepConsultaError(f"CEP {cep} não encontrado")

    monkeypatch.setattr(
        "src.manager.ocorrencia_manager.consultar_cep", fake_consultar_cep_erro
    )

    response = client.post("/ocorrencia", json=ocorrencia_payload)

    assert response.status_code == 400
    assert response.get_json()["success"] is False
    assert response.get_json()["message"] == f"CEP 01310100 não encontrado"

def test_deletar_ocorrencia(client, ocorrencia_payload):
    """Teste: ocorrência é removida com sucesso e some da listagem."""
    criacao = client.post("/ocorrencia", json=ocorrencia_payload)
    ocorrencia_id = criacao.get_json()["data"]["id"]

    resposta = client.delete(f"/ocorrencia/{ocorrencia_id}")

    assert resposta.status_code == 200
    assert resposta.get_json()["success"] is True


def test_deletar_ocorrencia_inexistente(client):
    """Teste: deletar um id que não existe retorna 404."""
    resposta = client.delete("/ocorrencia/id-que-nao-existe")

    assert resposta.status_code == 404
    assert resposta.get_json()["success"] is False
    assert resposta.get_json()["message"] == "Ocorrência não encontrada"
