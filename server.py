from concurrent import futures
import grpc
import imagegen_pb2
import imagegen_pb2_grpc
from diffusers import StableDiffusionPipeline
import torch
import io

class ImageGenService(imagegen_pb2_grpc.ImageGenServiceServicer):
    def __init__(self):
        self.pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4", 
            torch_dtype=torch.float32
        ).to("cpu")

    def Generate(self, request, context):
        prompt = request.prompt
        image = self.pipe(prompt).images[0]

        img_bytes = io.BytesIO()
        image.save(img_bytes, format='PNG')
        return imagegen_pb2.ImageResponse(image_data=img_bytes.getvalue())

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    imagegen_pb2_grpc.add_ImageGenServiceServicer_to_server(ImageGenService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
