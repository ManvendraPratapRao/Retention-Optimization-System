# --- 1. Base Image ---
FROM python:3.11-slim

WORKDIR /app

# --- 2. Create Data Volume Directory ---
RUN mkdir -p /app/data

# --- 3. Dependencies ---
COPY requirements-api.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-api.txt

# --- 4. Application Code ---
COPY . .

# --- 5. Runtime Config ---
EXPOSE 8000
ENV PORT=8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]