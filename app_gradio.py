"""
Gradio app for Hugging Face Spaces deployment.
This wraps the ML model in a Gradio interface for easy deployment.
Matches the Flask UI design exactly.
"""
import gradio as gr
import torch
from PIL import Image
import os
import base64
from io import BytesIO
from huggingface_hub import hf_hub_download

# Import model utilities
from model_utils import load_model, predict_image
from transformers import CLIPProcessor

# Configuration
# Set your model repository ID here (format: "username/model-repo-name")
# Example: "your-username/lymphoma-classifier-model"
MODEL_REPO_ID = os.getenv("MODEL_REPO_ID", "YOUR_USERNAME/lymphoma-classifier-model")
MODEL_FILENAME = "lymphoma_clip_classifier.pth"

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
CLASS_NAMES = ['DLBCL', 'Follicular', 'Hodgkin']

# Load model and processor at startup
print("Loading ML model from Hugging Face Hub...")
print(f"Model repository: {MODEL_REPO_ID}")
print(f"Using device: {DEVICE}")

try:
    # Download model from Hugging Face Hub
    print(f"Downloading model file: {MODEL_FILENAME}")
    model_path = hf_hub_download(
        repo_id=MODEL_REPO_ID,
        filename=MODEL_FILENAME,
        cache_dir=None  # Download to current directory
    )
    print(f"Model downloaded to: {model_path}")
    
    # Load the model
    ml_model = load_model(model_path, device=DEVICE)
    ml_processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
    print("Model loaded successfully!")
    model_loaded = True
except Exception as e:
    print(f"Error loading model: {e}")
    print(f"Make sure MODEL_REPO_ID is set correctly: {MODEL_REPO_ID}")
    model_loaded = False
    ml_model = None
    ml_processor = None

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def classify_and_format(image):
    """
    Classify image and format result as HTML matching Flask UI.
    """
    if image is None:
        return "<div class='placeholder-message'><p>Upload an image to see prediction results</p></div>"
    
    if not model_loaded:
        return "<div class='placeholder-message'><p style='color: #ef4444;'>Error: Model not loaded. Please check the deployment logs.</p></div>"
    
    try:
        # Save image temporarily
        temp_path = "temp_image.jpg"
        if isinstance(image, Image.Image):
            image.save(temp_path)
        else:
            img = Image.fromarray(image)
            img.save(temp_path)
        
        # Run inference
        prediction, confidence, description = predict_image(
            model=ml_model,
            image_path=temp_path,
            processor=ml_processor,
            device=DEVICE,
            class_names=CLASS_NAMES
        )
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        # Format as HTML matching Flask UI
        img_base64 = image_to_base64(image)
        result_html = f"""
        <div class="result-content">
            <img src="data:image/jpeg;base64,{img_base64}" class="result-image" alt="Uploaded image">
            <div class="prediction-label">{prediction}</div>
            <div class="confidence-score"><strong>Confidence:</strong> {confidence}</div>
            <div class="prediction-description"><strong>Description:</strong> {description}</div>
        </div>
        """
        return result_html
        
    except Exception as e:
        return f"<div class='placeholder-message'><p style='color: #ef4444;'>Error during classification: {str(e)}</p></div>"

# Custom CSS to match Flask UI exactly
custom_css = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: #f5f5f5;
    color: #333;
    line-height: 1.6;
}

/* Header Section */
.header-gradient {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #a855f7 100%);
    padding: 2rem 0;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    margin: -1rem -1rem 2rem -1rem;
    border-radius: 0;
}

.header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: white;
    margin-bottom: 0.5rem;
}

.header-subtitle {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.9);
}

.header-nav {
    display: flex;
    gap: 2rem;
}

.nav-link {
    color: white;
    text-decoration: none;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: opacity 0.3s;
}

.nav-link:hover {
    opacity: 0.8;
}

/* Main Content */
.main-content {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 2rem;
}

.content-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 3rem;
}

/* Panel Styles */
.panel {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.panel-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
    margin-bottom: 1rem;
}

.panel-instruction {
    color: #666;
    margin-bottom: 1.5rem;
}

/* Upload Panel */
.upload-zone {
    border: 2px dashed #ccc;
    border-radius: 8px;
    padding: 3rem 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
    margin-bottom: 1.5rem;
    background-color: #fafafa;
}

.upload-zone:hover {
    border-color: #667eea;
    background-color: #f0f0ff;
}

.upload-icon {
    font-size: 3rem;
    color: #667eea;
    margin-bottom: 1rem;
    display: block;
}

.upload-text {
    color: #666;
    font-size: 1rem;
}

/* Button styling - target Gradio button structure with multiple selectors */
button.upload-button,
button.upload-button.primary,
.upload-button button,
button[class*="upload-button"],
.gr-button.upload-button,
button.gr-button.upload-button {
    width: 100% !important;
    background-color: #1e40af !important;
    background: #1e40af !important;
    color: white !important;
    border: none !important;
    padding: 1rem 2rem !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: background-color 0.3s !important;
    margin-bottom: 1rem !important;
}

button.upload-button:hover,
button.upload-button.primary:hover,
.upload-button button:hover,
button[class*="upload-button"]:hover,
.gr-button.upload-button:hover,
button.gr-button.upload-button:hover {
    background-color: #1e3a8a !important;
    background: #1e3a8a !important;
}

/* Additional selector for Gradio's internal button structure */
.gr-button-wrapper button.upload-button,
.gr-form button.upload-button {
    background-color: #1e40af !important;
    background: #1e40af !important;
}

.upload-button:active {
    transform: scale(0.98) !important;
}

.supported-formats {
    color: #999;
    font-size: 0.9rem;
    text-align: center;
}

/* Result Panel */
.result-panel {
    min-height: 500px;
}

.result-content {
    width: 100%;
}

.placeholder-message {
    text-align: center;
    color: #999;
    padding: 3rem 0;
    font-size: 1.1rem;
}

.result-image {
    width: 100%;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.prediction-label {
    font-size: 1.3rem;
    font-weight: bold;
    color: #10b981 !important;
    margin-bottom: 0.5rem;
}

.confidence-score {
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 1rem;
}

.confidence-score strong {
    font-weight: bold;
    color: #333;
}

.prediction-description {
    color: #555;
    line-height: 1.6;
    font-size: 0.95rem;
}

.prediction-description strong {
    font-weight: bold;
    color: #333;
}

/* Feature Cards */
.feature-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    margin-bottom: 3rem;
}

.feature-card {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.feature-icon {
    font-size: 2.5rem;
    color: #667eea;
    margin-bottom: 1rem;
    display: block;
}

.feature-title {
    font-size: 1.2rem;
    font-weight: bold;
    color: #333;
    margin-bottom: 0.5rem;
}

.feature-description {
    color: #666;
    font-size: 0.95rem;
}

/* Footer */
.footer {
    background: white;
    border-top: 1px solid #e5e5e5;
    padding: 2rem 0;
    margin-top: 3rem;
}

.footer-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.footer-left, .footer-right {
    color: #666;
    font-size: 0.9rem;
}

.footer-left strong {
    color: #333;
}

/* Responsive Design */
@media (max-width: 968px) {
    .content-container {
        grid-template-columns: 1fr;
    }
    
    .feature-cards {
        grid-template-columns: 1fr;
    }
    
    .header-content {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }
}
"""

# Create Gradio interface with custom styling
with gr.Blocks(title="Lymphoma Classification", css=custom_css, theme=gr.themes.Default()) as demo:
    # Add Font Awesome CSS and icon styling in the head
    demo.head = """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* Ensure Font Awesome icons display */
        .fas, .fa {
            font-family: "Font Awesome 6 Free" !important;
            font-weight: 900 !important;
        }
    </style>
    """
    # Header
    with gr.Column(elem_classes="header-gradient"):
        with gr.Row(elem_classes="header-content"):
            with gr.Column(scale=2):
                gr.HTML("""
                    <h1 class="header-title">Lymphoma Classification</h1>
                    <p class="header-subtitle">AI-Powered Lymphoma Detection with Flask</p>
                """)
            with gr.Column(scale=1, min_width=200):
                gr.HTML("""
                    <div class="header-nav">
                        <a href="#" class="nav-link"><i class="fas fa-user"></i> About</a>
                        <a href="#" class="nav-link"><i class="fas fa-phone"></i> Contact</a>
                    </div>
                """)
    
    # Main content
    with gr.Column(elem_classes="main-content"):
        # Two-column layout
        with gr.Row(elem_classes="content-container"):
            # Left Panel: Upload
            with gr.Column(elem_classes="panel upload-panel"):
                gr.HTML("""
                    <h2 class="panel-title">Upload Tissue Image</h2>
                    <p class="panel-instruction">Choose a histopathology image to classify.</p>
                """)
                
                image_input = gr.Image(
                    label="",
                    type="pil",
                    height=300,
                    show_label=False
                )
                
                classify_btn = gr.Button("Upload Image", variant="primary", elem_classes="upload-button")
                
                gr.HTML("""
                    <p class="supported-formats">Supported formats: JPG, PNG, WebP</p>
                """)
            
            # Right Panel: Result
            with gr.Column(elem_classes="panel result-panel"):
                gr.HTML("""
                    <h2 class="panel-title">Prediction Result</h2>
                """)
                
                result_output = gr.HTML(
                    value="<div class='placeholder-message'><p>Upload an image to see prediction results</p></div>",
                    elem_classes="result-content"
                )
        
        # Feature Cards
        with gr.Row(elem_classes="feature-cards"):
            with gr.Column(elem_classes="feature-card"):
                gr.HTML("""
                    <div style="text-align: center;">
                        <i class="fas fa-tachometer-alt" style="font-size: 2.5rem; color: #667eea; margin-bottom: 1rem; display: block;"></i>
                        <h3 class="feature-title">Quick and Accurate</h3>
                        <p class="feature-description">Get instant and precise lymphoma classification results.</p>
                    </div>
                """)
            
            with gr.Column(elem_classes="feature-card"):
                gr.HTML("""
                    <div style="text-align: center;">
                        <i class="fas fa-cog" style="font-size: 2.5rem; color: #667eea; margin-bottom: 1rem; display: block;"></i>
                        <h3 class="feature-title">How It Works</h3>
                        <p class="feature-description">Upload an image and see the AI model's prediction.</p>
                    </div>
                """)
            
            with gr.Column(elem_classes="feature-card"):
                gr.HTML("""
                    <div style="text-align: center;">
                        <i class="fas fa-brain" style="font-size: 2.5rem; color: #667eea; margin-bottom: 1rem; display: block;"></i>
                        <h3 class="feature-title">Model Info</h3>
                        <p class="feature-description">Trained on histopathology images for lymphoma diagnosis.</p>
                    </div>
                """)
        
        # Footer
        gr.HTML("""
            <div class="footer">
                <div class="footer-content">
                    <p class="footer-left">Powered by <strong>Flask & AI</strong></p>
                    <p class="footer-right">© 2026 LymphoDetect</p>
                </div>
            </div>
        """)
    
    # Connect events
    classify_btn.click(
        fn=classify_and_format,
        inputs=image_input,
        outputs=result_output
    )
    
    image_input.upload(
        fn=classify_and_format,
        inputs=image_input,
        outputs=result_output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
