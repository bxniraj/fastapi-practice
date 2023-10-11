# DOCKER

# Create virtual env and activate it

python3 -m venv venv

source venv/bin/activate

# Install the requirement

pip install -r requirements.txt

# Run Server
uvicorn src.main:create_app --host 0.0.0.0 --port 8000 --reload --factory


docker run --name postgres -e POSTGRES_PASSWORD=postgres -d postgres

# Build docker container
docker-compose up -d --build

# Create a Postgres database
docker compose up

# Run docker container
`docker run -d -p 80:80 postgres`

# Stop docker container
`docker stop postgres`


# ALEMBIC

`alembic init alembic`

`alembic revision --autogenerate -m "user"`

`alembic upgrade head`


