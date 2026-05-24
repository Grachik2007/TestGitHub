from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, AsyncGenerator
import json
import uuid
from datetime import datetime

router = APIRouter()

AGENTS_DATA = {
    "seo": {
        "id": "seo",
        "name": "🔍 SEO Agent",
        "type": "seo",
        "description": "Анализ ключевых слов и оптимизация контента",
        "status": "active",
        "tasks": 1234,
        "successRate": 98.5,
        "created_at": "2024-01-01T00:00:00Z",
    },
    "supplier": {
        "id": "supplier",
        "name": "🏭 Supplier Agent",
        "type": "supplier",
        "description": "Поиск и анализ поставщиков",
        "status": "active",
        "tasks": 567,
        "successRate": 95.2,
        "created_at": "2024-01-01T00:00:00Z",
    },
    "product": {
        "id": "product",
        "name": "📦 Product Agent",
        "type": "product",
        "description": "Исследование трендов и товаров",
        "status": "active",
        "tasks": 892,
        "successRate": 96.8,
        "created_at": "2024-01-01T00:00:00Z",
    },
    "parser": {
        "id": "parser",
        "name": "🛒 Wonderfulbed Parser",
        "type": "parser",
        "description": "Парсинг товаров с ctradei для wonderfulbed.ru",
        "status": "active",
        "tasks": 45,
        "successRate": 99.1,
        "created_at": "2024-01-01T00:00:00Z",
    },
    "pricing": {
        "id": "pricing",
        "name": "💰 Pricing Agent",
        "type": "pricing",
        "description": "Оптимизация цен и анализ конкурентов",
        "status": "idle",
        "tasks": 234,
        "successRate": 94.7,
        "created_at": "2024-01-01T00:00:00Z",
    },
}


class AgentBase(BaseModel):
    name: str
    type: str
    description: Optional[str] = None


class AgentCreate(AgentBase):
    pass


class Agent(AgentBase):
    id: str
    status: str
    created_at: str

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    agent_id: str
    prompt: str
    parameters: Optional[dict] = None


class TaskResponse(BaseModel):
    task_id: str
    agent_id: str
    status: str
    result: Optional[dict] = None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    context: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    message: str
    task_id: str
    timestamp: str


async def generate_agent_response(agent_id: str, message: str) -> AsyncGenerator[str, None]:
    """Generate streaming response from agent."""
    agent = AGENTS_DATA.get(agent_id)
    if not agent:
        yield json.dumps({"error": "Agent not found"})
        return

    agent_name = agent["name"].split(" ")[1]

    responses = {
        "seo": [
            f"Анализирую ваш запрос '{message}' с точки зрения SEO... ",
            "Ключевые слова: найдено 15 релевантных терминов ",
            "Рекомендация 1: Оптимизация заголовков H1 ",
            "Рекомендация 2: Увеличение внутренних ссылок ",
            "Рекомендация 3: Улучшение скорости загрузки страницы",
        ],
        "supplier": [
            f"Ищу поставщиков для '{message}'... ",
            "Найдено 12 потенциальных поставщиков ",
            "Топ 1: ООО 'ТрейдПро' - цена $45, количество 1000 шт ",
            "Топ 2: ИП 'Логистик+' - цена $38, количество 5000 шт ",
            "Топ 3: Компания 'БизнесПлюс' - цена $42, количество 2000 шт",
        ],
        "product": [
            f"Исследую тренды для '{message}'... ",
            "Текущий спрос: высокий (↑ 23% за неделю) ",
            "Конкурентность: средняя (15 основных конкурентов) ",
            "Рекомендуемая цена: $45-55 ",
            "Прогноз: спрос будет расти в течение 3 месяцев",
        ],
        "parser": [
            f"Парсю товары по запросу '{message}'... ",
            "Найдено 342 товара в ctradei ",
            "Обновляю цены и остатки... ",
            "Синхронизирую с wonderfulbed.ru... ",
            "✅ Синхронизация завершена успешно. Обновлено 342 товара",
        ],
        "pricing": [
            f"Оптимизирую цены для '{message}'... ",
            "Анализирую конкурентов... ",
            "Базовая цена: $100 ",
            "После расчета маржи и расходов: $156.50 ",
            "Рекомендация: установить цену $155 для конкурентности",
        ],
    }

    agent_response = responses.get(agent_id, [f"Обработка запроса '{message}'...", "Анализ завершен", "✅ Готово"])

    for line in agent_response:
        yield json.dumps({"content": line}) + "\n"


@router.get("/", response_model=List[Agent])
async def list_agents():
    """List all available agents."""
    return list(AGENTS_DATA.values())


@router.post("/", response_model=Agent)
async def create_agent(agent: AgentCreate):
    """Create a new agent."""
    return {
        "id": "agent-1",
        "name": agent.name,
        "type": agent.type,
        "description": agent.description,
        "status": "active",
        "created_at": "2024-01-01T00:00:00Z",
    }


@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    """Get agent details."""
    agent = AGENTS_DATA.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.post("/{agent_id}/execute", response_model=TaskResponse)
async def execute_agent(agent_id: str, task: TaskCreate):
    """Execute an agent task."""
    if agent_id not in AGENTS_DATA:
        raise HTTPException(status_code=404, detail="Agent not found")

    return {
        "task_id": str(uuid.uuid4()),
        "agent_id": agent_id,
        "status": "completed",
        "result": {"response": "Task executed successfully"},
    }


@router.post("/{agent_id}/chat")
async def chat_with_agent(agent_id: str, request: ChatRequest):
    """Chat with agent - returns streaming response."""
    if agent_id not in AGENTS_DATA:
        raise HTTPException(status_code=404, detail="Agent not found")

    return StreamingResponse(
        generate_agent_response(agent_id, request.message),
        media_type="application/x-ndjson",
    )


@router.get("/{agent_id}/tasks", response_model=List[TaskResponse])
async def get_agent_tasks(agent_id: str):
    """Get agent execution history."""
    if agent_id not in AGENTS_DATA:
        raise HTTPException(status_code=404, detail="Agent not found")

    return [
        {
            "task_id": f"task-{i}",
            "agent_id": agent_id,
            "status": "completed",
            "result": {"response": f"Task result {i}"},
        }
        for i in range(1, 4)
    ]
