#  ImageGen AI: Text-to-Image Generation with gRPC + REST

ImageGen AI is a microservice-based application that generates images from textual prompts using a **Stable Diffusion** model. It showcases **gRPC communication**, a **REST gateway**, **Docker-based deployment**, and supports **HTML UI and Postman testing**.

---

##  Tech Stack

-  **Stable Diffusion** – Text-to-image generation model
-  **gRPC** – High-performance communication between services
-  **FastAPI**/**Flask** – Optional REST gateway for easier access
-  **Docker & Docker Compose** – Containerized deployment
-  **Postman** – API testing
-  **HTML Templates** – Simple web UI (optional)

---

##  Project Structure

| File/Folder | Description |
|-------------|-------------|
| `server.py` | gRPC backend server serving image generation |
| `client/` | gRPC client scripts to test locally |
| `http_gateway/` | REST gateway (Flask or FastAPI) forwarding to gRPC backend |
| `imagegen.proto` | gRPC service definitions: request & response format |
| `imagegen_pb2.py` & `imagegen_pb2_grpc.py` | Auto-generated gRPC code |
| `app.py` | Combined runner for gRPC + UI server (for simple local testing) |
| `templates/` | Contains HTML file for browser-based prompt input |
| `generated_image/` | Stores saved/generated images |
| `Dockerfile` | Builds the gRPC server container |
| `docker-compose.yml` | Orchestrates server, gateway, and UI |
| `docker-compose.debug.yml` | Dev-friendly setup with hot reloading |
| `.dockerignore` | Avoids copying unnecessary files into Docker |
| `requirements.txt` | Python dependencies (Diffusers, gRPC, Flask, etc.) |
| `imagegen.postman_collection.json` | Postman collection to test REST API |

---

##  Installation & Setup

### 1 Clone and Setup Virtual Environment

```bash
git clone <repo-url>
cd <repo-name>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
