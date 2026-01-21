# Lymphoma Classification Flask App

A Flask web application for classifying histopathology images of lymphoma subtypes.

## Features

- Clean, modern UI matching the design specification
- Image upload with drag-and-drop support
- Dummy model mode for testing (always returns DLBCL with random confidence 90-99.99%)
- Easy switching between dummy and real ML model modes
- Real-time prediction display with confidence scores

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Upload an image by clicking the upload zone or dragging and dropping an image
2. The app will classify the image:
   - **Dummy Mode (default)**: Always returns "Diffuse Large B-Cell Lymphoma" with a random confidence between 90.00% and 99.99%
   - **Real ML Mode**: Uses the trained ML model for actual classification

## Switching Between Dummy and Real ML Model

The app supports two modes that can be easily switched:

### Dummy Model Mode (Default)
Currently active. Always returns DLBCL with random confidence for testing/demo purposes.

### Real ML Model Mode
The ML model is fully implemented! To switch to the real ML model:

1. Open `app.py`
2. Change line 14 from:
   ```python
   app.config['MODEL_MODE'] = 'DUMMY'
   ```
   to:
   ```python
   app.config['MODEL_MODE'] = 'REAL'
   ```
3. Ensure the model file exists at `model/lymphoma_clip_classifier.pth`

The app uses a CLIP-based classifier that combines OpenAI's CLIP vision encoder with a custom classification head. The model will automatically load when the app starts in REAL mode.

## Project Structure

```
Lymphoma_AI/
├── app.py                 # Flask application
├── model_utils.py        # ML model utilities and CLIPClassifier class
├── model/
│   └── lymphoma_clip_classifier.pth  # Trained model weights
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css    # Stylesheet
│   └── js/
│       └── main.js      # JavaScript for interactions
└── uploads/             # Uploaded images (created automatically)
```

## Model Modes

- **DUMMY Mode**: Returns "Diffuse Large B-Cell Lymphoma" with random confidence (90.00-99.99%) for any image. Perfect for testing the UI and workflow.
- **REAL Mode**: Uses the actual trained CLIP-based ML model for classification. The model classifies images into three lymphoma subtypes:
  - **DLBCL** (Diffuse Large B-Cell Lymphoma)
  - **Follicular** (Follicular Lymphoma)
  - **Hodgkin** (Hodgkin Lymphoma)

## Technical Details

The ML model is a CLIP-based classifier that:
- Uses OpenAI's CLIP-ViT-Large-Patch14 as the vision encoder
- Adds a deep classification head (768 → 1024 → 512 → 256 → 3 classes)
- Automatically uses GPU if available, falls back to CPU otherwise
- Loads once at application startup for efficient inference

## Deployment to Hugging Face Spaces

This app is ready to deploy to Hugging Face Spaces (perfect for large model files)!

**Quick Start:**
1. See **[QUICK_START_HF.md](QUICK_START_HF.md)** for 5-minute deployment guide
2. See **[HF_SPACES_DEPLOYMENT.md](HF_SPACES_DEPLOYMENT.md)** for detailed instructions

**Why Hugging Face Spaces?**
- ✅ **FREE** - No credit card required
- ✅ **Large File Support** - Perfect for your large model file
- ✅ **Easy Setup** - Just upload files
- ✅ **Automatic HTTPS** - Secure by default

The repository includes:
- `app_gradio.py` - Gradio interface for HF Spaces
- `requirements_hf.txt` - Dependencies for Spaces (rename to `requirements.txt`)
- `README_HF_SPACES.md` - Space description (rename to `README.md`)
