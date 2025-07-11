# syntax=docker/dockerfile:1.4

#########################
# Stage 1: Build Stage
#########################

FROM python:3.10-slim as builder

LABEL maintainer="Your Name <you@example.com>"
LABEL description="FrameFlow build stage: installs dependencies."

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libffi-dev libssl-dev ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

# Set work directory
WORKDIR /app

# Copy project metadata first for caching
COPY pyproject.toml setup.cfg README.md LICENSE ./

# Upgrade pip, setuptools, wheel
RUN pip install --upgrade pip setuptools wheel

# Copy entire project for installation
COPY frameflow/ ./frameflow

# Install FrameFlow as a package into build environment
RUN pip install .

#########################
# Stage 2: Production Stage
#########################

FROM python:3.10-slim as production

LABEL maintainer="Your Name <you@example.com>"
LABEL description="FrameFlow: Transcribe technical videos into structured How-To documents with frames."

# Install runtime dependencies only
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

# Create non-root user
RUN useradd -m frameflowuser

# Set work directory
WORKDIR /app

# Copy installed site-packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project files (optional if you want CLI script only, include if configs or data are needed)
COPY frameflow/ ./frameflow

# Change ownership to non-root user
RUN chown -R frameflowuser:frameflowuser /app

# Switch to non-root user
USER frameflowuser

# Default entrypoint
ENTRYPOINT ["frameflow"]
CMD ["--help"]
