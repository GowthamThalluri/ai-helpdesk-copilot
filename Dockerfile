# 1. Start with an official Python runtime.
FROM python:3.13-slim

# 2. Improve Python behavior inside a container.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the application's working directory.
WORKDIR /app

# 4. Copy dependencies first to improve build-cache reuse.
COPY requirements.txt .

# 5. Install the application's runtime dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy backend and frontend files into the image.
COPY backend ./backend
COPY frontend ./frontend

# 7. Create a non-root user for the application.
RUN addgroup --system app \
    && adduser --system --ingroup app app \
    && chown -R app:app /app

USER app

# 8. Document the port used by the API server.
EXPOSE 8000

# 9. Start FastAPI using Uvicorn.
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]