# superset_config.py
# Configuration for Apache Superset on Render with Supabase + n8n integration

from datetime import timedelta
import os

# ========================
# Render-Specific Settings
# ========================
# Render provides environment variables for dynamic configuration
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "https://superset.onrender.com")
SECRET_KEY = os.getenv("SECRET_KEY", "your-render-specific-secret-key-here")

# ========================
# Database Configuration
# ========================
# For Supabase PostgreSQL integration
SQLALCHEMY_DATABASE_URI = os.getenv(
    "SUPABASE_DB_URI",
    "postgresql://postgres:your-supabase-password@db.supabase.com:5432/postgres"
)

# ========================
# API & Security Settings
# ========================
# Enable REST API for n8n integration
REST_API_ENABLED = True
WTF_CSRF_ENABLED = False  # Disable if using API-only access
PUBLIC_ROLE_LIKE = "Gamma"  # Adjust based on your needs

# CORS settings for n8n/webhook access
ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "resources": ["*"],
    "origins": ["*"]  # Restrict in production!
}

# JWT authentication for API
JWT_COOKIE_SECURE = True
JWT_TOKEN_LOCATION = ["headers"]
JWT_SECRET_KEY = SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

# ========================
# Feature Flags
# ========================
FEATURE_FLAGS = {
    # Enable API and dynamic dashboard creation
    "EMBEDDED_SUPERSET": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ALERT_REPORTS": True,
    "DASHBOARD_RBAC": True,
    
    # Required for n8n integration
    "THUMBNAILS": True,
    "LISTVIEWS_DEFAULT_CARD_VIEW": True,
}

# ========================
# Cache Configuration
# ========================
# Recommended for Render's ephemeral storage
CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_URL": os.getenv("REDIS_URL", "redis://localhost:6379/0")
}

DATA_CACHE_CONFIG = {
    **CACHE_CONFIG,
    "CACHE_KEY_PREFIX": "superset_data_"
}

# ========================
# Async Queries (Optional)
# ========================
ENABLE_ASYNC_QUERIES = True
RESULTS_BACKEND = {
    "type": "redis",
    "url": os.getenv("REDIS_URL", "redis://localhost:6379/0")
}

# ========================
# Custom Settings
# ========================
# Allow JSON data parsing from PostgreSQL
ALLOW_JSON = True

# Enable dashboard export/import
ENABLE_DASHBOARD_IMPORT = True
ENABLE_DASHBOARD_EXPORT = True

# ========================
# Logging
# ========================
LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
LOG_LEVEL = "DEBUG" if os.getenv("FLASK_ENV") == "development" else "INFO"

# ========================
# Render-Specific Extras
# ========================
# Health check endpoint (required for Render)
HEALTH_CHECK_PATH = "/health"

# Worker configuration (adjust based on Render instance size)
WORKERS = 4 if os.getenv("ENVIRONMENT") == "production" else 1
