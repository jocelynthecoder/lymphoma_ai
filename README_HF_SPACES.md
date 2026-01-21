---
title: Lymphoma Classification
emoji: 🩺
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 4.0.0
app_file: app_gradio.py
pinned: false
license: mit
---

# Lymphoma Classification

AI-powered web application for classifying histopathology images of lymphoma subtypes using CLIP-based deep learning.

## Features

- 🎯 **Three Lymphoma Subtypes**: DLBCL, Follicular, and Hodgkin
- 🤖 **CLIP-Based Model**: Uses OpenAI's CLIP-ViT-Large-Patch14
- 📊 **Confidence Scores**: Real-time prediction with confidence percentages
- 🖼️ **Easy Upload**: Drag-and-drop or click to upload images
- ⚡ **Fast Inference**: Optimized for quick predictions

## How to Use

1. Upload a histopathology image (JPG, PNG, or WebP)
2. Click "Classify Image" or wait for auto-classification
3. View the prediction, confidence score, and description

## Model Details

- **Architecture**: Deep CLIP Classifier
- **Base Model**: CLIP-ViT-Large-Patch14
- **Classes**: 3 (DLBCL, Follicular, Hodgkin)
- **Input**: Histopathology images
- **Output**: Classification with confidence score

## Technical Stack

- PyTorch
- Transformers (Hugging Face)
- CLIP (OpenAI)
- Gradio

## License

MIT License
