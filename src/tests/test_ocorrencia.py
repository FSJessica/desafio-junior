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

def test_create_ocorrencia_data_futura(client, ocorrencia_payload):
    """Teste: dataOcorrencia no futuro retorna 400."""
    payload = copy.deepcopy(ocorrencia_payload)
    payload["dataOcorrencia"] = "2099-01-01"

    response = client.post("/ocorrencia", json=payload)

    assert response.status_code == 400
    assert response.get_json()["success"] is False

def test_create_ocorrencia_cep_invalido(client, ocorrencia_payload):
    """Teste: CEP com menos de 8 dígitos retorna 400."""
    payload = copy.deepcopy(ocorrencia_payload)
    payload["cep"] = "123"

    response = client.post("/ocorrencia", json=payload)

    assert response.status_code == 400
    assert response.get_json()["success"] is False

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

