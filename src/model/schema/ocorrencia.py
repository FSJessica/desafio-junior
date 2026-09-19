# schemas Pydantic (entrada e saída)

from datetime import date
from typing import Literal

from pydantic import BaseModel,Field,field_validator

class OcorrenciaInputSchema(BaseModel):
    placa: str = Field(..., description="Placa do veículo (formato AAA9A99 ou AAA9999)")
    tipo: Literal["AVARIA", "MANUTENCAO", "MULTA"] = Field(..., description="Tipo da ocorrência")
    descricao: str = Field(..., min_length=5, max_length=255, description="Descrição da ocorrência")

    @field_validator("placa")
    @classmethod
    def validar_placa(cls, valor: str) -> str:
        import re
        padrao = r"^[A-Z]{3}\d[A-Z]\d{2}$|^[A-Z]{3}\d{4}$"
        if not re.match(padrao, valor.upper()):
            raise ValueError("Placa inválida. Use o formato AAA9A99 ou AAA9999")
        return valor.upper()