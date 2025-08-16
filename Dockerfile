FROM python:3.11-slim

WORKDIR /app

# Cài dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Expose port & run server
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
