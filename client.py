from flask import Flask, render_template, request, send_file
import grpc
import imagegen_pb2
import imagegen_pb2_grpc
import io

app = Flask(__name__)

# Function to communicate with gRPC server
def generate_image(prompt):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = imagegen_pb2_grpc.ImageGenServiceStub(channel)
        request = imagegen_pb2.ImageRequest(prompt=prompt)
        response = stub.Generate(request)
        return io.BytesIO(response.image_data)

# Route to render HTML form and receive user input
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        image_bytes = generate_image(prompt)
        return send_file(image_bytes, mimetype='image/png')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
