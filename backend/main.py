# C:\Projetos\TP1\backend\main.py

from fastapi import FastAPI, HTTPException, status
from typing import List
from models import EventSchema, EventOutSchema # Importa os Schemas
from bson import ObjectId # CORRIGIDO: Importa ObjectId

# ----------------- Estrutura da API (Simulação de CRUD) -----------------

app = FastAPI(
    title="Biblioteca Digital de Artigos - API",
    description="API para gerenciamento de Eventos, Edições e Artigos Científicos.",
    version="0.1.0",
)

# Simulando um banco de dados temporário para o Contrato (Lista Python)
db_simulado = []


# 1. Endpoint POST /events (Criar Evento)
@app.post(
    "/events",
    response_model=EventOutSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo Evento.",
)
async def create_event(event_data: EventSchema):
    """
    Recebe os dados de um novo evento e o cria no banco de dados.
    """
    # Cria o objeto de saída, simulando o ID gerado pelo MongoDB
    novo_evento = EventOutSchema(**event_data.model_dump(), _id=ObjectId())
    
    # Se estivéssemos implementando a lógica, aqui seria o 'insert'
    db_simulado.append(novo_evento)
    
    return novo_evento


# 2. Endpoint GET /events (Listar Todos)
@app.get(
    "/events",
    response_model=List[EventOutSchema], # Contrato: Deve retornar uma lista
    summary="Lista todos os Eventos.",
)
async def list_events():
    """
    Retorna uma lista de todos os eventos cadastrados.
    """
    # Retorna os dados do banco simulado para definir o contrato
    return db_simulado


# 3. Endpoint GET /events/{slug} (Detalhe)
@app.get(
    "/events/{slug}",
    response_model=EventOutSchema,
    summary="Retorna os detalhes de um Evento pelo seu slug.",
)
async def get_event_detail(slug: str):
    """
    Busca um evento específico usando seu slug (identificador de URL).
    """
    # Simula a busca no DB
    for event in db_simulado:
        if event.slug == slug:
            return event

    raise HTTPException(status_code=404, detail="Evento não encontrado")


# 4. Endpoint DELETE /events/{slug} (Deletar)
@app.delete(
    "/events/{slug}",
    status_code=status.HTTP_204_NO_CONTENT, # Contrato: Sem conteúdo na resposta
    summary="Deleta um Evento.",
)
async def delete_event(slug: str):
    """
    Remove permanentemente um evento.
    """
    # Simula a lógica de deleção
    global db_simulado
    db_simulado = [e for e in db_simulado if e.slug != slug]
    return


# 5. Endpoint PUT /events/{slug} (Atualizar)
@app.put(
    "/events/{slug}",
    response_model=EventOutSchema,
    summary="Atualiza completamente um Evento existente.",
)
async def update_event(slug: str, event_data: EventSchema):
    """
    Atualiza todos os campos de um evento existente.
    """
    # Simula a lógica de atualização
    for idx, event in enumerate(db_simulado):
        if event.slug == slug:
            # Cria um novo objeto com os dados atualizados
            updated_event = EventOutSchema(**event_data.model_dump(), _id=event.id)
            db_simulado[idx] = updated_event
            return updated_event
            
    raise HTTPException(status_code=404, detail="Evento não encontrado para atualização")