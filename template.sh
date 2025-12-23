mkdir -p app
mkdir -p app/core
mkdir -p app/api
mkdir -p app/api/v1
mkdir -p app/schemas
mkdir -p app/services

touch .env
touch .gitignore
touch Dockerfile
touch docker-compose.yml

touch app/__init__.py
touch app/main.py

touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/api/v1/endpoints.py

touch app/core/__init__.py
touch app/core/config.py
touch app/core/database.py

touch app/schemas/__init__.py
touch app/schemas/ingestion.py
touch app/services/chat.py

