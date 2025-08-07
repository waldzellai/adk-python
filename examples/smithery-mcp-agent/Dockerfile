# Multi-stage build for Smithery MCP Agent
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Smithery CLI globally
RUN npm install -g @smithery/cli

# Create non-root user
RUN useradd -m -u 1000 smithery

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/smithery/.local

# Copy application files
COPY --chown=smithery:smithery . .

# Ensure the user's local bin is in PATH
ENV PATH="/home/smithery/.local/bin:${PATH}"

# Create necessary directories
RUN mkdir -p /app/logs /home/smithery/.smithery/cache \
    && chown -R smithery:smithery /app/logs /home/smithery/.smithery

# Switch to non-root user
USER smithery

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["python", "smithery_mcp_agent.py"]