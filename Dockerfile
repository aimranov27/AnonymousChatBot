FROM python:3.11-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .

# Install build dependencies for matplotlib
RUN apk add --no-cache build-base gfortran python3-dev freetype-dev libpng-dev jpeg-dev musl-dev zlib-dev openblas-dev

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup . .
USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]