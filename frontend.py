import gradio as gr
from PIL import Image
import random

# Generate 3 dummy images with random colors (can be replaced by real generation logic)
def generate_images_from_text(prompt, style, variation, motifs):
    images = []
    for _ in range(3):
        img = Image.new('RGB', (512, 512), (
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        images.append(img)
    return images

# Navigation toggle functions
def switch_to_home():
    return gr.update(visible=True), gr.update(visible=False)

def switch_to_main():
    return gr.update(visible=False), gr.update(visible=True)

# Main app function
def main_app():
    with gr.Blocks(css="""
        .home-background {
            background-image: url('https://img.freepik.com/free-vector/hand-drawn-flat-design-boho-wall-art_23-2149271830.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            min-height: 100vh;
            width: 100%;
        }
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background-color: rgba(255, 255, 255, 0.9);
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
            z-index: 100;
        }
        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            color: #2e2f30;
        }
        .nav-buttons {
            display: flex;
            gap: 20px;
        }
        .gr-button {
            background: none !important;
            border: none !important;
            font-size: 1.1rem !important;
            font-weight: 600;
            cursor: pointer;
            color: #2eb67d !important;
        }
        .gr-button:hover {
            color: #e5ab86 !important;
        }
        #home-btn, #img-btn {
            background-color: #e5ab86 !important;
            color: black !important;
            border: none !important;
            border-radius: 10px;
            font-weight: bold;
            padding: 10px 20px;
        }
        #home-btn:hover, #img-btn:hover {
            background-color: #a7d9d4 !important;
        }
    """) as app:

        # Navigation bar
        with gr.Row(elem_id="navbar", elem_classes="navbar"):
            gr.HTML("<div class='logo'>CreativityX</div>")
            with gr.Row(elem_classes="nav-buttons"):
                home_btn = gr.Button("🏠 Home", elem_id="home-btn")
                main_btn = gr.Button("🎨 Image Generation", elem_id="img-btn")

        # Home Page
        with gr.Column(visible=True, elem_classes="home-background") as home_page:
            gr.HTML("""
                <div class="content-section">
                    <section id="home" style="position: relative; min-height: 100vh;">
                        <div style="position: absolute; top: 20px; left: 50%; transform: translateX(-50%); text-align: center;">
                            <h1 style="font-size: 2.8rem; font-weight: 700; color: #1d1d1d; white-space: nowrap; font-family: 'Libre Baskerville', serif;">
                                Where Imagination Becomes Reality
                            </h1>
                        </div>
                        <div style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; flex-wrap: wrap; justify-content: center;">
                            <input type="email" placeholder="Enter your email" style="padding: 15px; font-size: 1rem; border: 1px solid #ccc; border-radius: 5px; width: 300px;">
                            <button style="padding: 15px 30px; background-color: #e5ab86; color: black; font-size: 1rem; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">
                                Get Started
                            </button>
                        </div>
                    </section>
                </div>
            """)

        # Image Generation Page
        with gr.Column(visible=False) as main_page:
            gr.HTML("""
                <div class="content-section" style="max-width: 700px; margin: auto;">
                    <section id="main" style="min-height: 100vh; padding-top: 100px;">
                        <div style="margin-bottom: 30px; display: flex; justify-content: center;">
                            <div style="
                                width: 100%;
                                max-width: 728px;
                                padding: 20px;
                                font-size: 1.8 rem;
                                font-weight: bold;
                                background: linear-gradient(90deg, #e60073, #6600ff);
                                -webkit-background-clip: text;
                                -webkit-text-fill-color: transparent;
                                text-align: center;">
                                🎨 Text to Image Generator
                            </div>
                        </div>

                        <div style="width: 100%; display: flex; gap: 10px; overflow-x: auto; padding-bottom: 20px;">
                            <img src="https://wallpapercat.com/w/full/b/d/0/2147694-3840x2160-desktop-4k-fantasy-art-background-image.jpg" style="height: 500px; border-radius: 0px;">
                            <img src="https://www.pixelstalk.net/wp-content/uploads/images6/Fantasy-Wallpaper-Free-Download.jpg" style="height: 500px; border-radius: 0px;">
                            <img src="https://wallpapers.com/images/featured/fantasy-art-background-q69qeisi4hzce5w7.jpg" style="height: 500px; border-radius: 0px;">
                        </div>
                    </section>
                </div>
            """)

            with gr.Column(elem_id="prompt-area", scale=1, min_width=500):
                prompt = gr.Textbox(placeholder="Enter your creative prompt...", label="Your Prompt", lines=2)

                style_input = gr.Textbox(placeholder="Choose a style (1 to 8)", label="Style Option (1–8)", lines=1)
                variation_input = gr.Textbox(placeholder="Describe any variation you'd like", label="Variation", lines=2)
                motifs_input = gr.Textbox(placeholder="Specify any cultural motifs", label="Cultural Motifs", lines=2)

                generate_btn = gr.Button("Generate Images")

                with gr.Row():
                    output_image1 = gr.Image(label="Image Style 1", type="pil")
                    output_image2 = gr.Image(label="Image Style 2", type="pil")
                    output_image3 = gr.Image(label="Image Style 3", type="pil")

                generate_btn.click(
                    generate_images_from_text,
                    inputs=[prompt, style_input, variation_input, motifs_input],
                    outputs=[output_image1, output_image2, output_image3]
                )

        # Navigation
        home_btn.click(fn=switch_to_home, outputs=[home_page, main_page])
        main_btn.click(fn=switch_to_main, outputs=[home_page, main_page])

    app.launch(server_port=8665)

if _name_ == "_main_":
    main_app()