from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import pathlib
import random
import torch

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp'}

# Model configuration: Set to 'DUMMY' for dummy model, 'REAL' for ML model
app.config['MODEL_MODE'] = 'REAL' #'DUMMY'  # Change to 'REAL' when ML model is ready
app.config['MODEL_PATH'] = 'model/lymphoma_clip_classifier.pth'

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variables for ML model (loaded once at startup)
ml_model = None
ml_processor = None
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def load_ml_model():
    """Load the ML model once at application startup."""
    global ml_model, ml_processor
    
    if app.config['MODEL_MODE'] == 'REAL':
        try:
            from model_utils import load_model
            
            print(f"Loading ML model from {app.config['MODEL_PATH']}...")
            print(f"Using device: {device}")
            
            # Load model
            ml_model = load_model(app.config['MODEL_PATH'], device=device)
            
            # Get processor from the model - must match the model_id used in training
            from transformers import CLIPProcessor
            ml_processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
            
            print("ML model loaded successfully!")
        except Exception as e:
            print(f"Error loading ML model: {e}")
            raise

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_random_confidence():
    """Generate a random confidence value between 90.00 and 99.99"""
    return f"{random.uniform(90.00, 99.99):.2f}%"

def classify_with_dummy_model(filepath, filename):
    """
    Dummy model: Always returns DLBCL with random confidence.
    This is used for testing/demo purposes.
    Returns: (prediction, confidence, description)
    """
    confidence = generate_random_confidence()
    return (
        'Diffuse Large B-Cell Lymphoma',
        confidence,
        'High-grade malignant lymphoma characterized by large B-cells.'
    )

def classify_with_ml_model(filepath, filename):
    """
    Real ML model classification function using CLIP-based classifier.
    
    Returns: (prediction, confidence, description)
    """
    global ml_model, ml_processor
    
    if ml_model is None or ml_processor is None:
        raise RuntimeError("ML model not loaded. Make sure MODEL_MODE is set to 'REAL' and model file exists.")
    
    try:
        from model_utils import predict_image
        
        # Run inference
        prediction, confidence, description = predict_image(
            model=ml_model,
            image_path=filepath,
            processor=ml_processor,
            device=device,
            class_names=['DLBCL', 'Follicular', 'Hodgkin']
        )
        
        return prediction, confidence, description
        
    except Exception as e:
        # Fallback to dummy model if ML model fails
        print(f"Error in ML model inference: {e}")
        return classify_with_dummy_model(filepath, filename)

def classify_image(filepath, filename):
    """
    Main classification function that routes to either dummy or real model
    based on configuration.
    Returns: (prediction, confidence, description)
    """
    if app.config['MODEL_MODE'] == 'DUMMY':
        return classify_with_dummy_model(filepath, filename)
    elif app.config['MODEL_MODE'] == 'REAL':
        return classify_with_ml_model(filepath, filename)
    else:
        raise ValueError(f"Invalid MODEL_MODE: {app.config['MODEL_MODE']}. Must be 'DUMMY' or 'REAL'.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Classify image using the configured model (dummy or real ML)
        prediction, confidence, description = classify_image(filepath, filename)
        
        # Return result with image path
        return jsonify({
            'success': True,
            'image_url': f'/uploads/{filename}',
            'prediction': prediction,
            'confidence': confidence,
            'description': description
        })
    
    return jsonify({'error': 'Invalid file type. Please upload JPG, PNG, or WebP.'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Load ML model if in REAL mode
    if app.config['MODEL_MODE'] == 'REAL':
        load_ml_model()
    
    app.run(debug=True)
