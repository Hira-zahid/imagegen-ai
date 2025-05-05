# ImageGen AI - Text-to-Image Microservice

A microservice-based text-to-image generation system built using:

- gRPC for high-performance backend communication  
- REST (Flask) gateway for user interaction  
- Diffusers + Stable Diffusion for image generation  
- Docker and `docker-compose` for seamless deployment  
- Postman for API testing  
- Gradio-compatible architecture  

---

## Features

- Generate images from text prompts  
- Communicate via gRPC, REST, or UI  
- Flask web interface with gRPC backend  
- Dockerized and production-ready  
- Pre-integrated with `CompVis/stable-diffusion-v1-4`  

---

## Project Structure

| File/Folder               | Description                                   |
|--------------------------|-----------------------------------------------|
| `app.py`                 | Flask UI + gRPC server in one unified file    |
| `server.py`              | gRPC-only backend server (optional split)     |
| `client/`                | gRPC client code (optional for test scripts)  |
| `http_gateway/`          | Flask REST gateway calling gRPC backend       |
| `templates/index.html`   | Simple HTML form for text input               |
| `imagegen.proto`         | gRPC service definition (used for codegen)    |
| `imagegen_pb2*.py`       | Auto-generated gRPC Python bindings           |
| `requirements.txt`       | Python dependencies                           |
| `Dockerfile`             | Image for server setup                        |
| `docker-compose.yml`     | Compose setup to launch REST & gRPC           |
| `.dockerignore`          | Docker ignore file                            |
| `generated_image/`       | Folder for output images                      |
| `imagegen.postman_collection.json` | Postman collection for API testing   |

---

## Setup Instructions

### 1. Install Dependencies


pip install -r requirements.txt
# ImageGen AI - Text-to-Image Generation

This project demonstrates a microservice-based architecture for generating images from text prompts using:

- gRPC backend
- Flask REST gateway
- HuggingFace Diffusers (Stable Diffusion)
- Dockerized deployment
- Postman support for testing

---

##  Requirements

- Python 3.9+
- pip
- Optional: Docker and Docker Compose (for containerized setup)

Install dependencies:


pip install -r requirements.txt
### Project Structure
File/Folder	Description
# 1. app.py	Unified gRPC + Flask server (default entry)
# 2.server.py	gRPC server only (optional split)
# 3.client/	Optional gRPC client example code
# 4.http_gateway/app.py	REST API Gateway only (optional split)
# 5.templates/index.html	Web form for user prompt
# 6.imagegen.proto	gRPC service definition
# 7.imagegen_pb2*.py	gRPC auto-generated Python files
# 8.generated_image/	Folder where generated images are saved
# 9.imagegen.postman_collection.json	Postman test collection
# 10.Dockerfile	Docker build file
# 11.docker-compose.yml	Multi-service Docker setup

## How to Run the Project
 # Method 1: Run Locally without Docker
Use this if you're running on your machine (CPU or GPU).

# Step 1: Install Python Requirements
bash
Copy
Edit
pip install -r requirements.txt
(If not included: pip install torch torchvision diffusers flask grpcio grpcio-tools)

# Step 2: Start the Server
You have two options:

# Option A: Combined Flask + gRPC (RECOMMENDED)

Copy
Edit
python app.py
Runs Flask on http://localhost:5000

Runs gRPC server on port 50051

Visit http://localhost:5000 to generate images via UI

# Option B: Run gRPC and REST Separately (Advanced)
Start gRPC server:

bash
Copy
Edit
python server.py
In a new terminal, run the REST API Gateway:

bash
Copy
Edit
python http_gateway/app.py
Now:

gRPC server on localhost:50051

Flask REST API on http://localhost:5000

# Method 2: Run with Docker
No need to install Python or dependencies locally.

#  Step 1: Build the Docker image
bash
Copy
Edit
docker build -t imagegen .
# Step 2: Run the container
bash
Copy
Edit
docker run -p 5000:5000 -p 50051:50051 imagegen
Visit http://localhost:5000 to access the UI.

# Method 3: Use Docker Compose (Multi-container Setup)
bash
Copy
Edit
docker-compose up --build
Starts both gRPC and REST containers

REST API at http://localhost:5000

gRPC service at localhost:50051

 ` How to Use the API (Postman)`
Import imagegen.postman_collection.json into Postman.

Use the POST /generate endpoint.

Body (JSON):

json
Copy
Edit
{
  "prompt": "a dragon flying over a city",
  "style": "Fantasy"
}
Send request → server responds with path to generated image.

 Notes
Generated images are saved in generated_image/

You can modify the default model in app.py (currently uses CompVis/stable-diffusion-v1-4)

CPU generation is slow – for real-time performance, run with GPU

` Troubleshooting `
Issue	Fix
diffusers errors	Make sure transformers, accelerate, and diffusers are installed
grpcio import fails	Reinstall with pip install grpcio grpcio-tools
Docker build too slow	Ensure Docker has access to enough memory (6–8 GB)
