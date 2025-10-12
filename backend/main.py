# C:\Projetos\TP1\backend\main.py

from fastapi import FastAPI, HTTPException, status
from typing import List# C:\Projetos\TP1\backend\main.py

from fastapi import FastAPI, HTTPException, status
from typing import List
from models import EventSchema, EventOutSchema # Importa os Schemas Pydantic
from bson import ObjectId
from database import event_collection # <--- NOVIDADE: Importa a coleção real do MongoDB

# ----------------- FUNÇÃO HELPER (Converte DB -> Pydantic) -----------------

def event_helper(event) -> dict:
    """Converte o objeto retornado pelo MongoDB (BSON) para um dicionário Python que 
    se encaixa no schema de saída do Pydantic (EventOutSchema)."""
    
    # Usa 'str(event["_id"])' para garantir que o ObjectId seja serializado para string
    # E os campos datetime são convertidos para string ISO (o Pydantic lida com isso)
    return {
        "id": str(event["_id"]),
        "name": event["name"],
        "slug": event["slug"],
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

# REMOVIDO: db_simulado = []


# 1. Endpoint POST /events (Criar Evento) - Lógica ainda simulada
@app.post(
    "/events",
    response_model=EventOutSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo Evento.",
)
async def create_event(event_data: EventSchema):
    """Aqui você fará a inserção real no MongoDB na Task 4."""
    # Simulação da criação para manter o contrato da API
    novo_evento = EventOutSchema(**event_data.model_dump(), _id=ObjectId())
    
    # db_simulado.append(novo_evento) # Removido
    
    return novo_evento


# 2. Endpoint GET /events (Listar Todos) - AGORA COM LÓGICA DE DB
@app.get(
    "/events",
    response_model=List[EventOutSchema],
    summary="Lista todos os Eventos.",
)
async def list_events():
    """
    Busca e retorna uma lista de todos os eventos cadastrados no MongoDB.
    """
    if event_collection is None:
        # Se a conexão falhou no startup, a API retorna 503
        raise HTTPException(status_code=503, detail="Serviço indisponível: Conexão com o banco de dados falhou.")

    events_list = []
    
    # Busca todos os documentos na coleção 'events'
    # O .find() retorna um cursor PyMongo
    cursor = event_collection.find()
    
    # Itera sobre o cursor e aplica o helper para converter para o formato Pydantic
    for event in cursor:
        events_list.append(event_helper(event))

    return events_list # Retorna a lista de eventos (pode ser vazia)


# 3. Endpoint GET /events/{slug} (Detalhe) - Ainda simulado
@app.get(
    "/events/{slug}",
    response_model=EventOutSchema,
    summary="Retorna os detalhes de um Evento pelo seu slug.",
)
async def get_event_detail(slug: str):
    """
    Busca um evento específico usando seu slug (identificador de URL).
    """
    # Lógica de busca real será implementada na Task 4
    raise HTTPException(status_code=404, detail="Busca não implementada (Task 4)")


# 4. Endpoint DELETE /events/{slug} (Deletar) - Ainda simulado
@app.delete(
    "/events/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um Evento.",
)
async def delete_event(slug: str):
    """Lógica de deleção será implementada na Task 4."""
    return


# 5. Endpoint PUT /events/{slug} (Atualizar) - Ainda simulado
@app.put(
    "/events/{slug}",
    response_model=EventOutSchema,
    summary="Atualiza completamente um Evento existente.",
)
async def update_event(slug: str, event_data: EventSchema):
    """Lógica de atualização será implementada na Task 4."""
    raise HTTPException(status_code=404, detail="Atualização não implementada (Task 4)")
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