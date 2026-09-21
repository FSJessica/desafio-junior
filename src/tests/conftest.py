import pytest
import json
from pathlib import Path

from src.app import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as test_client:
        yield test_client

@pytest.fixture(autouse=True)
def mock_consultar_cep(monkeypatch):
    def fake_consultar_cep(cep):
        return {
            "logradouro": "Rua Teste",
            "bairro": "Bairro Teste",
            "localidade": "Cidade Teste",
            "uf": "TS",
        }

    monkeypatch.setattr(
        "src.manager.ocorrencia_manager.consultar_cep", fake_consultar_cep
    )

@pytest.fixture
def ocorrencia_payload():
    caminho = Path(__file__).parent / "resources" / "ocorrencia_payload.json"
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)