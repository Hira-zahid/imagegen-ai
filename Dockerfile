# Use a lightweight official Python image
FROM python:3.10-slim

# Install system packages needed by diffusers and PIL
RUN apt-get update && apt-get install -y \
    git \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install pip packages manually (no requirements.txt)
RUN pip install --no-cache-dir \
    grpcio \
    grpcio-tools \
    protobuf \
    diffusers \
    #torch \
    transformers \
    accelerate \
    safetensors \
    Pillow

# (Optional) Download model to cache so container is ready on startup
RUN python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('CompVis/stable-diffusion-v1-4')"

# Expose gRPC server port
EXPOSE 50051

# Start the gRPC server
CMD ["python", "server.py"]
