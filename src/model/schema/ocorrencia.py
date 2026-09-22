# schemas Pydantic (entrada e saída)

from datetime import date
from typing import Literal

from pydantic import BaseModel,Field,field_validator

class OcorrenciaInputSchema(BaseModel):
    placa: str = Field(..., description="Placa do veículo (formato AAA9A99 ou AAA9999)")
    tipo: Literal["AVARIA", "MANUTENCAO", "MULTA"] = Field(..., description="Tipo da ocorrência")
    descricao: str = Field(..., min_length=5, max_length=255, description="Descrição da ocorrência")
    dataOcorrencia: date = Field(..., description="Data em que a ocorrência aconteceu")
    cep: str = Field(..., description="CEP para consulta de endereço (com ou sem máscara)")

    @field_validator("placa")
    @classmethod
    def validar_placa(cls, valor: str) -> str:
        import re
        padrao = r"^[A-Z]{3}\d[A-Z]\d{2}$|^[A-Z]{3}\d{4}$"
        if not re.match(padrao, valor.upper()):
            raise ValueError("Placa inválida. Use o formato AAA9A99 ou AAA9999")
        return valor.upper()

    @field_validator("dataOcorrencia")
    @classmethod
    def validar_data_nao_futura(cls, valor: date) -> date:
        if valor > date.today():
            raise ValueError("A data da ocorrência não pode ser no futuro")
        return valor

    @field_validator("cep")
    @classmethod
    def validar_cep(cls, valor: str) -> str:
        cep_limpo = valor.replace("-", "").replace(".", "").strip()
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            raise ValueError("CEP inválido. Use o formato 99999999 ou 99999-999")
        return cep_limpo