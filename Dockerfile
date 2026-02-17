# Multi-stage build for test automation framework
# Use the official Playwright image to include all browser deps
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy as base

# Set working directory
WORKDIR /app

# Playwright image already includes all browser dependencies

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies and ensure browser deps are present
USER root
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install-deps chromium && \
    playwright install chromium

# Copy application code
COPY . .

# Create output directories with correct ownership
USER root
RUN mkdir -p allure-results tests/screenshots && \
    chown -R pwuser:pwuser /app
USER pwuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command runs tests
CMD ["pytest", "-v", "--alluredir=allure-results"]
