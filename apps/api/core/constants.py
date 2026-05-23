# Agent types
AGENT_TYPES = {
    "seo": "SEO Analysis Agent",
    "supplier": "Supplier Research Agent",
    "product": "Product Research Agent",
    "pricing": "Pricing Optimization Agent",
}

# Task statuses
TASK_STATUS_PENDING = "pending"
TASK_STATUS_PROCESSING = "processing"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_FAILED = "failed"
TASK_STATUS_CANCELLED = "cancelled"

TASK_STATUSES = [
    TASK_STATUS_PENDING,
    TASK_STATUS_PROCESSING,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_FAILED,
    TASK_STATUS_CANCELLED,
]

# User roles
ROLE_ADMIN = "admin"
ROLE_USER = "user"
ROLE_GUEST = "guest"

ROLES = [ROLE_ADMIN, ROLE_USER, ROLE_GUEST]

# API configuration
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
