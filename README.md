# Histopathology Image Classification for Lymphoma Diagnosis using Large Language and Visual Models

Histopathology images are microscopic images of tissues used by pathologists to diagnose diseases, especially cancer. These images, typically obtained from stained tissue sections, reveal cellular components and structures. In this project, I use large language models (LLMs) and vision models to improve the efficiency and accuracy of lymphoma diagnosis.

I have experimented
- Classify lymphoma images using LLMs with **prompt engineering** and how the prompt affects image-based reasoning
  - Design **safe, structured prompts** for medical AI research
  - Use **few-shot and contrastive prompting** to improve consistency

- Classify lymphoma images using **CLIP model** and a customized **deep neural network**
  - Zero-shot learning with CLIP model
  - Few-shot learning with CLIP model
  - Training a deep neural network after the CLIP model

In addition, I have deployed the best performing model as a web app on [Hugging Face Spaces](https://huggingface.co/spaces/jocelynthecoder/lymphoma-classifier), providing real-time predictions, confidence scores, and interpretable outputs for scalable, accessible clinical integration.

Data used in this project is downloaded from Webpathology.com and Wikipedia. [Google drive link](https://drive.google.com/drive/folders/1l28Poe6R_R7_OVGDLyV4HUX8SAJS_Mfe)
