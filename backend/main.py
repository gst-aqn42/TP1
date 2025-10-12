# C:\Projetos\TP1\backend\main.py

from fastapi import FastAPI, HTTPException, status
from typing import List, Optional
from models import EventSchema, EventOutSchema # Schemas Pydantic
from bson import ObjectId
from database import event_collection # A coleção real do MongoDB

# ----------------- FUNÇÕES HELPER -----------------

def check_db_availability():
    """Verifica se a coleção do DB está acessível e levanta 503 caso contrário."""
    if event_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Serviço indisponível: Conexão com o banco de dados falhou."
        )

def event_helper(event) -> dict:
    """Converte o documento BSON do MongoDB para um dicionário Pydantic (EventOutSchema)."""
    
    # Esta função é crucial para a saída. O PyMongo retorna "_id" (ObjectId) e datas como datetime.
    # Precisamos converter para "id" (str) e datas para o formato ISO string.
    return {
        "id": str(event["_id"]),
        "name": event["name"],
        "slug": event["slug"],
        # Usamos .get() para campos opcionais como 'description'
        "description": event.get("description"), 
        "start_date": event["start_date"].isoformat(), 
        "end_date": event["end_date"].isoformat(),
    }


# ----------------- ESTRUTURA DA API -----------------

app = FastAPI(
    title="Biblioteca Digital de Artigos - API",
    description="API para gerenciamento de Eventos, Edições e Artigos Científicos.",
    version="0.1.0",
)


# 1. Endpoint POST /events (CREATE)
@app.post(
    "/events",
    response_model=EventOutSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo Evento no MongoDB.",
)
async def create_event(event_data: EventSchema):
    check_db_availability()
    
    # 1. Converte o modelo Pydantic para um dicionário Python.
    # O Pydantic garante que todos os campos obrigatórios e formatos estão corretos.
    event_dict = event_data.model_dump()
    
    # 2. Verifica se o slug já existe (Unicidade é um requisito de negócio)
    if event_collection.find_one({"slug": event_dict["slug"]}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"O slug '{event_dict['slug']}' já está em uso por outro evento."
        )

    # 3. Insere o documento no MongoDB
    new_event = await event_collection.insert_one(event_dict)
    
    # 4. Busca o documento recém-inserido para obter o _id e retornar a saída
    created_event = await event_collection.find_one({"_id": new_event.inserted_id})
    
    # 5. Retorna o objeto formatado pelo helper
    return event_helper(created_event)


# 2. Endpoint GET /events (READ ALL)
@app.get(
    "/events",
    response_model=List[EventOutSchema],
    summary="Lista todos os Eventos.",
)
async def list_events():
    check_db_availability()
    
    events_list = []
    
    # Busca todos os documentos na coleção 'events'
    # O .find() retorna um cursor PyMongo
    cursor = event_collection.find()
    
    # Itera sobre o cursor e aplica o helper para converter para o formato Pydantic
    for event in cursor:
        events_list.append(event_helper(event))

    return events_list


# 3. Endpoint GET /events/{slug} (READ DETAIL)
@app.get(
    "/events/{slug}",
    response_model=EventOutSchema,
    summary="Retorna os detalhes de um Evento pelo seu slug.",
)
async def get_event_detail(slug: str):
    check_db_availability()
    
    # 1. Busca um único documento pelo campo 'slug'
    event = await event_collection.find_one({"slug": slug})

    if event:
        # 2. Se encontrado, retorna o objeto formatado
        return event_helper(event)
        
    # 3. Se não encontrado, levanta o erro 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Evento com slug '{slug}' não encontrado."
    )


# 4. Endpoint PUT /events/{slug} (UPDATE)
@app.put(
    "/events/{slug}",
    response_model=EventOutSchema,
    summary="Atualiza completamente um Evento existente (Todos os campos são obrigatórios).",
)
async def update_event(slug: str, event_data: EventSchema):
    check_db_availability()
    
    # 1. Converte o modelo de entrada para um dicionário
    update_data = event_data.model_dump()
    
    # 2. Usa update_one com o operador $set para atualizar os campos.
    # NOTA: O slug em 'update_data' será o mesmo, pois o Pydantic o exige.
    result = await event_collection.update_one(
        {"slug": slug}, 
        {"$set": update_data}
    )

    if result.modified_count == 1:
        # 3. Se a modificação foi bem-sucedida, busca o documento atualizado para retornar
        updated_event = await event_collection.find_one({"slug": slug})
        return event_helper(updated_event)
    
    # 4. Se modified_count for 0, o documento original não foi encontrado
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Evento com slug '{slug}' não encontrado para atualização."
    )


# 5. Endpoint DELETE /events/{slug} (DELETE)
@app.delete(
    "/events/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um Evento pelo seu slug.",
)
async def delete_event(slug: str):
    check_db_availability()
    
    # 1. Deleta um único documento baseado no slug
    result = await event_collection.delete_one({"slug": slug})
    
    if result.deleted_count == 0:
        # 2. Se deleted_count for 0, o documento não existia
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Evento com slug '{slug}' não encontrado para exclusão."
        )
    
    # 3. Retorna 204 No Content
    return