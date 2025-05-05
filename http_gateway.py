from flask import Flask, request, jsonify
import grpc
import imagegen_pb2
import imagegen_pb2_grpc

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt')
    style = data.get('style', 'Realistic')

    # gRPC connection
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = imagegen_pb2_grpc.ImageGenStub(channel)
        request_proto = imagegen_pb2.GenerationRequest(prompt=prompt, style=style)
        response = stub.Generate(request_proto)

    return jsonify({
        "status": response.status,
        "image_base64": response.image_data  # if it's base64 encoded
    })

if __name__ == '__main__':
    app.run(port=8000)
