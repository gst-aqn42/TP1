# C:\Projetos\TP1\backend\models.py

from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, validator
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

# ----------------- Customização do ID do MongoDB -----------------

class PyObjectId(ObjectId):
    """Permite que o Pydantic V2 valide e use o ObjectId do MongoDB."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    # NOVO MÉTODO V2: Gera o schema JSON como tipo "string" (substitui __modify_schema__)
    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


# ----------------- Schemas do Recurso Autor -----------------

class AuthorSchema(BaseModel):
    """Define o contrato de dados para um Autor."""
    name: str = Field(..., description="Nome completo do autor.")
    email: EmailStr = Field(..., description="E-mail do autor para notificações.")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Maria Eduarda",
                "email": "duda.pasquel@exemplo.com"
            }
        }

# ----------------- Schemas do Recurso Evento -----------------

# 1. Schema de Entrada e Atualização
class EventSchema(BaseModel):
    """Define o contrato de dados para a criação ou atualização de um Evento."""

    name: str = Field(..., description="Nome completo do evento.", min_length=3)
    # CORREÇÃO V2: Usamos 'pattern' em vez de 'regex'
    slug: str = Field(..., description="URL amigável e única (Ex: sbes)", min_length=3, pattern="^[a-z0-9-]+$")
    description: Optional[str] = Field(None, description="Breve descrição do evento.")
    start_date: datetime = Field(..., description="Data e hora de início do evento (Formato ISO 8601).")
    end_date: datetime = Field(..., description="Data e hora de término do evento (Formato ISO 8601).")
    
    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values, **kwargs):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('A data de término deve ser posterior à data de início.')
        return v

    class Config:
        # CORREÇÃO V2: 'schema_extra' -> 'json_schema_extra'
        json_schema_extra = {
            "example": {
                "name": "Congresso Nacional de Engenharia",
                "slug": "cne",
                "start_date": "2025-11-01T09:00:00Z",
                "end_date": "2025-11-05T18:00:00Z"
            }
        }


# 2. Schema de Saída (Incluindo o ID do DB)
class EventOutSchema(EventSchema):
    """Define o contrato de dados para a saída, incluindo o ID do MongoDB."""

    # O 'alias="_id"' mapeia o campo '_id' do MongoDB para 'id' no JSON de saída
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", description="ID gerado pelo MongoDB.")

    class Config:
        # CORREÇÃO V2: 'allow_population_by_field_name' -> 'populate_by_name'
        populate_by_name = True 
        
        # CORREÇÃO V2: Usamos o novo campo para exemplos de saída
        json_schema_extra = {
             "example": {
                "id": "60e1c0e0b3c6c0001f3e7b4e",
                "name": "Congresso Nacional de Engenharia",
                "slug": "cne",
                "start_date": "2025-11-01T09:00:00Z",
                "end_date": "2025-11-05T18:00:00Z"
            }
        }


# ----------------- Schemas do Recurso Edição -----------------

class EditionSchema(BaseModel):
    """Define o contrato de dados para uma Edição de Evento."""
    event_slug: str = Field(..., description="O SLUG do evento principal.")
    year: int = Field(..., description="O ano da edição (Ex: 2025).")
    pdf_upload_url: Optional[str] = Field(None, description="URL onde o arquivo PDF da edição está salvo.")


# ----------------- Schemas do Recurso Artigo -----------------

class ArticleSchema(BaseModel):
    """Define o contrato de dados para um Artigo Científico."""
    title: str = Field(..., description="Título completo do artigo.")
    abstract: str = Field(..., description="Resumo do artigo.")
    edition_year: int = Field(..., description="O ano da edição em que o artigo foi publicado.")
    edition_slug: str = Field(..., description="O slug do evento em que o artigo foi publicado.")
    authors: List[AuthorSchema] = Field(..., description="Lista dos autores do artigo.")
    pdf_url: Optional[str] = Field(None, description="URL para o arquivo PDF do artigo.")
    publication_date: datetime = Field(..., description="Data de publicação (Formato ISO 8601).")


# ----------------- Schemas do Recurso Inscrição/Notificação -----------------

class SubscriptionSchema(BaseModel):
    """Define o contrato de dados para o cadastro de notificações por e-mail."""
    email: EmailStr = Field(..., description="E-mail para recebimento de alertas de novos artigos.")