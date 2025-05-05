# app.py
from flask import Flask, render_template, request, send_file
from concurrent import futures
import threading
import grpc
import io
from PIL import Image
from diffusers import StableDiffusionPipeline
import torch
import imagegen_pb2
import imagegen_pb2_grpc

pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
pipe.to("cpu")

class ImageGenServicer(imagegen_pb2_grpc.ImageGenServicer):
    def Generate(self, request, context):
        prompt = request.prompt
        image = pipe(prompt).images[0]
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        return imagegen_pb2.GenReply(image=img_bytes.getvalue())

def start_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    imagegen_pb2_grpc.add_ImageGenServicer_to_server(ImageGenServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("🛰️ gRPC server running at port 50051")
    server.wait_for_termination()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        image = pipe(prompt).images[0]
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    return render_template("index.html")

if __name__ == "__main__":
    grpc_thread = threading.Thread(target=start_grpc, daemon=True)
    grpc_thread.start()
    app.run(debug=True, port=5000)
