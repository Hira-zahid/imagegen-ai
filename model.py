from diffusers import StableDiffusionXLPipeline, StableDiffusionPipeline
import torch
import matplotlib.pyplot as plt
import gc
import os
import time
from IPython.display import clear_output
from googletrans import Translator
import logging

# Configure logging for googletrans
logging.basicConfig(level=logging.ERROR)

# ================ CONFIG ================
MODEL_CONFIG = {
    "1": {"name": "Realistic", "model": "RunDiffusion/Juggernaut-XL-v9", "res": 768, "is_sdxl": True, "pipe": None},
    "2": {"name": "Semi-Real", "model": "stabilityai/stable-diffusion-xl-base-1.0", "res": 768, "is_sdxl": True, "pipe": None},
    "3": {"name": "Anime", "model": "gsdf/CounterfeitXL", "res": 768, "is_sdxl": True, "pipe": None},
    "4": {"name": "Fantasy", "model": "dreamlike-art/dreamlike-diffusion-1.0", "res": 768, "is_sdxl": False, "pipe": None},
    "5": {"name": "3D Cartoon", "model": "Lykon/dreamshaper-8", "res": 768, "is_sdxl": False, "pipe": None},
    "6": {"name": "Mythical", "model": "prompthero/openjourney", "res": 768, "is_sdxl": False, "pipe": None},
    "7": {"name": "RPG", "model": "nitrosocke/elden-ring-diffusion", "res": 768, "is_sdxl": False, "pipe": None},
    "8": {"name": "Default", "model": "stabilityai/stable-diffusion-xl-base-1.0", "res": 768, "is_sdxl": True, "pipe": None}
}

STYLE_PROMPTS = {
    "Realistic": "ultra realistic, 8K UHD, photorealistic",
    "Semi-Real": "realistic with artistic touch",
    "Anime": "anime style, vibrant colors, official art",
    "Fantasy": "magical atmosphere, intricate details, fantasy art",
    "3D Cartoon": "Pixar style, 3D render, vibrant colors",
    "Mythical": "mythological creature, divine lighting, epic composition",
    "RPG": "D&D character, dramatic lighting, RPG fantasy",
    "Default": "high quality, detailed"
}

# ================ ENHANCED STYLE SYSTEMS ================
STYLE_FUSION_OPTIONS = {
    "watercolor": "watercolor painting with visible brush strokes",
    "cyberpunk": "neon lighting, futuristic cityscape", 
    "ukiyo-e": "Japanese woodblock print style",
    "oil_painting": "thick oil paint texture, impasto technique",
    "pixel_art": "8-bit retro pixel art style",
    "low_poly": "low poly 3D game asset style"
}

CULTURAL_MOTIFS = {
    "japanese": "with cherry blossoms and kanji calligraphy",
    "indian": "with henna patterns and marigold flowers",
    "arabic": "with Islamic geometric borders",
    "nordic": "with rune carvings and fur textures",
    "chinese": "with cloud motifs and red lanterns",
    "african": "with Adinkra symbols and Kente patterns"
}

# Supported languages with their codes and display names
SUPPORTED_LANGUAGES = {
    'auto': 'Auto-detect',
    'en': 'English',
    'ur': 'Urdu (اردو)',
    'roman_ur': 'Roman Urdu',
    'hi': 'Hindi',
    'ar': 'Arabic',
    'tr': 'Turkish',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean'
}

# Special handling for Roman Urdu (common words mapping)
ROMAN_URDU_MAPPING = {
    "khubsurat": "beautiful",
    "tasveer": "picture",
    "manzar": "scenery",
    "dost": "friend",
    "pyaar": "love",
    "khushi": "happiness",
    "ghar": "house",
    "bara": "big",
    "chota": "small",
    "rang": "color"
}

# ================ GPU CONFIGURATION ================
def check_gpu():
    """Check if CUDA is available"""
    if not torch.cuda.is_available():
        print("❌ CUDA not available - GPU acceleration required")
        return False
    print(f"✅ Using GPU: {torch.cuda.get_device_name(0)}")
    return True

# ================ TRANSLATION SERVICE ================
def translate_to_english(text, src_lang='auto'):
    """Translate text to English with special handling for Roman Urdu and Urdu"""
    if src_lang == 'roman_ur':
        translated_words = []
        for word in text.split():
            lower_word = word.lower()
            if lower_word in ROMAN_URDU_MAPPING:
                translated_words.append(ROMAN_URDU_MAPPING[lower_word])
            else:
                translated_words.append(word)
        text = ' '.join(translated_words)
        
        try:
            translator = Translator()
            detected = translator.detect(text)
            if detected.lang != 'en':
                translation = translator.translate(text, src=detected.lang, dest='en')
                return translation.text
            return text
        except Exception as e:
            print(f"⚠ Translation error: {str(e)[:200]}")
            return text

    elif src_lang == 'ur':
        try:
            translator = Translator()
            translation = translator.translate(text, src='ur', dest='en')
            return translation.text
        except Exception as e:
            print(f"⚠ Urdu translation error: {str(e)[:200]}")
            return text

    elif src_lang == 'auto':
        try:
            translator = Translator()
            detected = translator.detect(text)
            if detected.lang == 'en':
                return text
            translation = translator.translate(text, src=detected.lang, dest='en')
            return translation.text
        except Exception as e:
            print(f"⚠ Auto-translation error: {str(e)[:200]}")
            return text

    else:
        try:
            translator = Translator()
            translation = translator.translate(text, src=src_lang, dest='en')
            return translation.text
        except Exception as e:
            print(f"⚠ {src_lang} translation error: {str(e)[:200]}")
            return text

def apply_style_fusion(prompt, base_style, fusion_style, strength=0.3):
    """Blends the base model style with an additional art style"""
    if fusion_style in STYLE_FUSION_OPTIONS:
        return f"{prompt}, {STYLE_PROMPTS[base_style]} blended with {STYLE_FUSION_OPTIONS[fusion_style]} (strength: {strength})"
    return prompt

def apply_cultural_motif(prompt, culture):
    """Adds cultural-specific artistic elements"""
    return f"{prompt} {CULTURAL_MOTIFS.get(culture, '')}"

def select_fusion_style():
    print("\n🎨 Available Style Fusions:")
    for i, style in enumerate(STYLE_FUSION_OPTIONS.keys(), 1):
        print(f"{i}. {style}")
    choice = input("\nSelect style to fuse (Enter to skip): ").strip()
    if choice.isdigit() and 0 < int(choice) <= len(STYLE_FUSION_OPTIONS):
        return list(STYLE_FUSION_OPTIONS.keys())[int(choice)-1]
    return None

def select_culture():
    print("\n🌍 Cultural Motifs:")
    for i, culture in enumerate(CULTURAL_MOTIFS.keys(), 1):
        print(f"{i}. {culture}")
    choice = input("\nSelect cultural motif (Enter to skip): ").strip()
    if choice.isdigit() and 0 < int(choice) <= len(CULTURAL_MOTIFS):
        return list(CULTURAL_MOTIFS.keys())[int(choice)-1]
    return None

# ================ MEMORY MANAGEMENT ================
def clear_memory():
    """GPU memory clearing"""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

# ================ GPU-ONLY MODEL LOADING ================
def load_model(choice):
    model = MODEL_CONFIG.get(choice, MODEL_CONFIG["8"])
    
    if model["pipe"] is not None:
        return model["pipe"], model
    
    clear_memory()
    print(f"⚙ Loading {model['name']} model...")
    
    try:
        kwargs = {
            "torch_dtype": torch.float16,
            "use_safetensors": True,
            "variant": "fp16" if model["is_sdxl"] else None
        }
        
        PipelineClass = StableDiffusionXLPipeline if model["is_sdxl"] else StableDiffusionPipeline
        pipe = PipelineClass.from_pretrained(model["model"], **kwargs)
        
        # Move to GPU and enable optimizations
        pipe = pipe.to("cuda")
        pipe.enable_attention_slicing(1)
        pipe.enable_sequential_cpu_offload()
        
        MODEL_CONFIG[choice]["pipe"] = pipe
        return pipe, model
    except Exception as e:
        print(f"⚠ Error loading model: {str(e)[:200]}")
        return None, None

# ================ IMAGE GENERATION ================
def generate_image(pipe, prompt, model_info, attempt=1, language='auto', fusion_style=None, culture=None):
    clear_memory()
    try:
        # Translation handling
        english_prompt = translate_to_english(prompt, src_lang=language)
        if english_prompt != prompt:
            lang_name = SUPPORTED_LANGUAGES.get(language, language)
            print(f"🌍 Translated from {lang_name}: {english_prompt}")
        
        # Apply enhancements
        if fusion_style:
            english_prompt = apply_style_fusion(english_prompt, model_info['name'], fusion_style)
        if culture:
            english_prompt = apply_cultural_motif(english_prompt, culture)
        
        print(f"🎨 Final Prompt: {english_prompt}")
        
        # Fixed resolution for GPU
        size = model_info["res"]
        
        print(f"🖼 Generating at {size}x{size} on GPU")
        
        generator = torch.Generator(device="cuda").manual_seed(int(time.time()))
        
        result = pipe(
            prompt=english_prompt,
            negative_prompt="blurry, deformed, bad anatomy, ugly, text",
            num_inference_steps=30,
            guidance_scale=7.0,
            width=size,
            height=size,
            generator=generator
        )
        return result.images[0]
    except torch.cuda.OutOfMemoryError:
        if attempt < 3:
            return generate_image(pipe, prompt, model_info, attempt+1, language, fusion_style, culture)
        print("⚠ Out of memory - try a simpler prompt")
        return None
    except Exception as e:
        print(f"⚠ Error: {str(e)[:200]}")
        return None

# ================ LANGUAGE SELECTION ================
def select_language():
    """Display language selection menu and return chosen language code"""
    print("\n🌐 Supported Languages:")
    lang_codes = sorted(SUPPORTED_LANGUAGES.keys())
    
    for i in range(0, len(lang_codes), 2):
        lang1 = lang_codes[i]
        lang2 = lang_codes[i+1] if i+1 < len(lang_codes) else None
        
        line = f"{lang1}. {SUPPORTED_LANGUAGES[lang1].ljust(15)}"
        if lang2:
            line += f"{lang2}. {SUPPORTED_LANGUAGES[lang2]}"
        print(line)
    
    while True:
        choice = input("\nEnter language code (or 'auto' for detection): ").strip().lower()
        if choice in SUPPORTED_LANGUAGES:
            return choice
        print("⚠ Invalid language code. Please try again.")

# ================ MAIN INTERFACE ================
def main():
    if not check_gpu():
        return
    
    # Environment setup
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "garbage_collection_threshold:0.8"
    torch.backends.cuda.matmul.allow_tf32 = True
    
    print("\n" + "="*50)
    print("🌟 AI Image Generator (GPU Edition)".center(50))
    print("="*50)
    
    print("\n💡 For Urdu: Enter text in Urdu script (اردو)")
    print("💡 For Roman Urdu: Use English letters (like 'khubsurat tasveer')")
    
    print("\nStyles:")
    for num in sorted(MODEL_CONFIG.keys()):
        print(f"{num}. {MODEL_CONFIG[num]['name']}")
    
    # Get language selection
    language = select_language()
    
    while True:
        try:
            # Get user input with language-specific prompt
            lang_name = SUPPORTED_LANGUAGES.get(language, language)
            prompt = input(f"\n🎨 Enter prompt in {lang_name} (or 'quit' to change language): ").strip()
            
            if prompt.lower() in ['quit', 'exit']:
                language = select_language()
                continue
            
            if not prompt:
                print("⚠ Please enter a prompt")
                continue
                
            choice = input("🖌 Style choice (1-8): ").strip()
            if choice not in MODEL_CONFIG:
                choice = "8"
                print("ℹ Using default style")
            
            # Get style fusion and cultural motifs
            fusion_style = select_fusion_style()
            culture = select_culture()
            
            # Load model
            pipe, model = load_model(choice)
            if pipe is None:
                print("⚠ Failed to load model")
                continue
            
            # Generate and display
            clear_output(wait=True)
            print(f"\n✨ Generating '{prompt}' in {model['name']} style...")
            
            plt.figure(figsize=(18, 6))
            images = []
            for i in range(3):
                img = generate_image(
                    pipe, 
                    prompt, 
                    model,
                    language=language,
                    fusion_style=fusion_style,
                    culture=culture
                )
                if img:
                    plt.subplot(1, 3, i+1)
                    plt.imshow(img)
                    plt.title(f"Variation {i+1}")
                    plt.axis('off')
                    images.append(img)
                else:
                    plt.subplot(1, 3, i+1)
                    plt.text(0.5, 0.5, "Failed to generate", ha='center')
                    plt.axis('off')
            
            plt.tight_layout()
            plt.show()
            
            # Continue prompt
            while True:
                cont = input("\nGenerate more with same language? (y/n/change): ").strip().lower()
                if cont in ['y', 'n', 'change']:
                    break
                print("Please enter 'y', 'n', or 'change'")
            
            if cont == 'n':
                print("\n🎨 Happy creating! Goodbye!")
                break
            elif cont == 'change':
                language = select_language()
                
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"\n⚠ Unexpected error: {str(e)[:200]}")
            time.sleep(2)
            continue

if _name_ == "_main_":
    main()