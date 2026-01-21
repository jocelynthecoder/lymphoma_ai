"""
Model utilities for CLIP-based lymphoma classifier.
"""
import torch
import torch.nn as nn
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import os

class DeepCLIPClassifier(nn.Module):
    """
    Deep CLIP-based classifier for lymphoma subtype classification.
    Matches the exact architecture used during training.
    """
    def __init__(self, model_id="openai/clip-vit-large-patch14", num_classes=3):
        super(DeepCLIPClassifier, self).__init__()
        
        # Load the base CLIP model
        self.clip_model = CLIPModel.from_pretrained(model_id)
        
        # Freeze CLIP weights (transfer learning)
        for param in self.clip_model.parameters():
            param.requires_grad = False
        
        # Get embedding dimension from CLIP's projection dimension
        embedding_dim = self.clip_model.config.projection_dim
        
        # Deep Classification Head
        # Added Batch Normalization to help the deep layers converge faster
        self.classifier = nn.Sequential(
            # Layer 1: Expansion or projection
            nn.Linear(embedding_dim, 1024),
            nn.BatchNorm1d(1024),
            nn.ReLU(),
            nn.Dropout(0.3),
            
            # Layer 2: Deep Processing
            nn.Linear(1024, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.3),
            
            # Layer 3: Feature Compression
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.2),
            
            # Output Layer
            nn.Linear(256, num_classes)
        )
        
    def forward(self, pixel_values):
        """
        Forward pass through CLIP vision encoder and classification head.
        
        Args:
            pixel_values: Preprocessed image tensors
            
        Returns:
            Logits for each class
        """
        # Extract the pre-projected embeddings from CLIP
        outputs = self.clip_model.get_image_features(pixel_values=pixel_values)
        
        # Ensure outputs are normalized if they aren't already
        outputs = outputs / outputs.norm(dim=-1, keepdim=True)
        
        return self.classifier(outputs)

def is_valid_image(filename):
    """
    Check if file is a valid image file.
    Filters out non-image files like .ipynb_checkpoints.
    """
    valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'}
    ext = os.path.splitext(filename.lower())[1]
    return ext in valid_extensions

def load_model(model_path, device='cpu'):
    """
    Load the trained Deep CLIP classifier model.
    
    Args:
        model_path: Path to the .pth model file
        device: Device to load model on ('cpu' or 'cuda')
        
    Returns:
        Loaded model in evaluation mode
    """
    # Initialize model architecture - must match training exactly
    model = DeepCLIPClassifier(model_id="openai/clip-vit-large-patch14", num_classes=3)
    
    # Load trained weights
    model.load_state_dict(torch.load(model_path, map_location=device))
    
    # Set to evaluation mode
    model.eval()
    
    # Move to device
    model = model.to(device)
    
    return model

def preprocess_image(image_path, processor):
    """
    Preprocess a single image for CLIP model inference.
    
    Args:
        image_path: Path to the image file
        processor: CLIP processor for image preprocessing
        
    Returns:
        Preprocessed image tensor ready for model input
    """
    # Load and convert to RGB if needed
    image = Image.open(image_path).convert('RGB')
    
    # Preprocess with CLIP processor
    inputs = processor(images=image, return_tensors="pt")
    
    return inputs['pixel_values']

def predict_image(model, image_path, processor, device='cpu', class_names=None):
    """
    Run inference on a single image.
    
    Args:
        model: Loaded DeepCLIPClassifier model
        image_path: Path to the image file
        processor: CLIP processor
        device: Device to run inference on
        class_names: List of class names in order [DLBCL, Follicular, Hodgkin]
        
    Returns:
        Tuple of (predicted_class_name, confidence_percentage, description)
    """
    if class_names is None:
        class_names = ['DLBCL', 'Follicular', 'Hodgkin']
    
    # Preprocess image
    pixel_values = preprocess_image(image_path, processor)
    pixel_values = pixel_values.to(device)
    
    # Run inference
    with torch.no_grad():
        logits = model(pixel_values)
        probabilities = torch.softmax(logits, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)
    
    # Get predicted class
    predicted_idx = predicted_idx.item()
    confidence_value = confidence.item() * 100
    
    # Map to class name
    class_name = class_names[predicted_idx]
    
    # Format class name for display
    class_display_names = {
        'DLBCL': 'Diffuse Large B-Cell Lymphoma',
        'Follicular': 'Follicular Lymphoma',
        'Hodgkin': 'Hodgkin Lymphoma'
    }
    
    # Get descriptions
    descriptions = {
        'DLBCL': 'High-grade malignant lymphoma characterized by large B-cells.',
        'Follicular': 'Indolent B-cell lymphoma with follicular growth pattern.',
        'Hodgkin': 'Lymphoma characterized by Reed-Sternberg cells.'
    }
    
    display_name = class_display_names.get(class_name, class_name)
    description = descriptions.get(class_name, 'Lymphoma subtype classification.')
    
    return display_name, f"{confidence_value:.2f}%", description
