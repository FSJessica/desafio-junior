import pytest

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