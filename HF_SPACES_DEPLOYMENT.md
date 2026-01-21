# Hugging Face Spaces Deployment Guide

Complete step-by-step guide for deploying your Lymphoma Classification app to Hugging Face Spaces.

## Why Hugging Face Spaces?

✅ **FREE** - No credit card required  
✅ **Large File Support** - Perfect for your large model file (no size restrictions like Railway)  
✅ **Easy Setup** - Just upload files and it works  
✅ **Automatic HTTPS** - Secure by default  
✅ **Public or Private** - Control who can access your app  

## Prerequisites

1. A Hugging Face account ([sign up here](https://huggingface.co/join))
2. Your model file: `lymphoma_clip_classifier.pth`
3. All project files ready

## ⚠️ Important: Model Storage

**Your model file is too large for Spaces (1GB limit).** We'll upload it to the **Hugging Face Models Hub** instead, which has no size restrictions for public models.

**Step 0: Upload Model to Models Hub (Do This First!)**

1. Go to [huggingface.co/new](https://huggingface.co/new)
2. Select **"Model"** (not Space)
3. Fill in:
   - **Model name**: `lymphoma-classifier-model` (or your choice)
   - **Visibility**: Public (recommended) or Private
4. Click **"Create model"**
5. In your model repository, click **"Add file"** → **"Upload file"**
6. Upload your `lymphoma_clip_classifier.pth` file
7. **Note your model repository ID**: `YOUR_USERNAME/lymphoma-classifier-model`
   - Example: `johndoe/lymphoma-classifier-model`

**This is a one-time setup. The model will be downloaded automatically by your Space.**

## Step-by-Step Deployment

### Step 1: Prepare Your Files

Make sure you have these files in your project:

```
Lymphoma_AI/
├── app_gradio.py          # Gradio interface (already created)
├── model_utils.py         # Model utilities
├── requirements_hf.txt    # Dependencies (rename to requirements.txt for Spaces)
├── README_HF_SPACES.md    # Space description (rename to README.md for Spaces)
├── model/
│   └── lymphoma_clip_classifier.pth  # Your trained model
└── .gitattributes         # For Git LFS (if model > 100MB)
```

### Step 2: Create a Hugging Face Account

1. Go to [huggingface.co](https://huggingface.co)
2. Click "Sign Up" (top right)
3. Create account (email or GitHub)
4. Verify your email

### Step 3: Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click the **"Create new Space"** button (top right)
3. Fill in the form:
   - **Space name**: `lymphoma-classifier` (or your choice)
   - **SDK**: Select **"Gradio"** ⚠️ Important!
   - **Hardware**: **CPU basic** (free) or upgrade to GPU
   - **Visibility**: **Public** (or Private)
4. Click **"Create Space"**

### Step 4: Upload Files via Web Interface

**Method 1: Web Upload (Easiest)**

1. In your Space page, go to **"Files and versions"** tab
2. Click **"Add file"** → **"Upload file"**

Upload these files one by one:

**Required Files:**
- `app_gradio.py` → Upload as-is
- `model_utils.py` → Upload as-is
- `requirements_hf.txt` → Upload and **rename to `requirements.txt`**
- `README_HF_SPACES.md` → Upload and **rename to `README.md`**

**⚠️ Model File:**
- **DO NOT upload the model file to the Space!** It's too large (exceeds 1GB limit).
- The model will be downloaded from the Models Hub automatically.

**Set Environment Variable:**
- Go to Space settings → **"Variables and secrets"**
- Add variable:
  - **Key**: `MODEL_REPO_ID`
  - **Value**: `YOUR_USERNAME/lymphoma-classifier-model` (your actual model repo ID from Step 0)
- Click **"Save"**

**Optional (for styling):**
- `static/css/style.css` (if you want custom styling)
- `static/js/main.js` (if needed)

3. After uploading, the Space will automatically:
   - Install dependencies from `requirements.txt`
   - Run `app_gradio.py`
   - Build and deploy your app

### Step 5: Monitor Deployment

1. Go to the **"Logs"** tab in your Space
2. Watch the build process:
   - Installing dependencies...
   - Loading model...
   - Starting Gradio server...
3. Wait 5-15 minutes for first deployment (model download takes time)
4. You'll see: "Running on local URL: http://0.0.0.0:7860"

### Step 6: Access Your Live App

Once deployed, your app is available at:
```
https://YOUR_USERNAME-lymphoma-classifier.hf.space
```

Example: `https://johndoe-lymphoma-classifier.hf.space`

## Alternative: Git-Based Deployment

If you prefer using Git:

### Step 1: Install Git LFS (for large files)

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.pth"
git lfs track "model/*.pth"
```

### Step 2: Prepare Repository

```bash
# Rename files for Spaces
cp requirements_hf.txt requirements.txt
cp README_HF_SPACES.md README.md

# Commit files
git add .
git commit -m "Prepare for HF Spaces deployment"
```

### Step 3: Push to Hugging Face

1. In your Space, go to **"Files and versions"** tab
2. Click **"Clone repository"** to get the Git URL
3. Add as remote and push:

```bash
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
git push hf main
```

## Configuration

### Hardware Options

- **CPU basic** (Free): Good for testing, slower inference
- **CPU upgrade** ($0.60/hour): Faster CPU, more RAM
- **T4 small** ($0.60/hour): GPU acceleration, much faster
- **A10G small** ($4.13/hour): High-end GPU for production

### Environment Variables

If needed, add in Space settings → **"Variables and secrets"**:
- `MODEL_MODE=REAL`
- `HF_TOKEN=your_token` (if using private models)

## Troubleshooting

### ❌ Model Not Loading

**Problem**: Error in logs about model file not found

**Solution**:
- Check model file is in `model/` folder
- Verify file name matches: `lymphoma_clip_classifier.pth`
- Check file size (should be uploaded completely)
- Look at logs for exact error message

### ❌ Out of Memory

**Problem**: App crashes with memory error

**Solution**:
- Upgrade to CPU upgrade or GPU tier
- Reduce batch size in model code
- Use CPU-only PyTorch build (smaller memory footprint)

### ❌ Slow Inference

**Problem**: Predictions take too long

**Solution**:
- Upgrade to GPU tier (T4 small)
- Model loads once, subsequent predictions are faster
- Consider optimizing model or using quantization

### ❌ Dependencies Not Installing

**Problem**: Build fails during pip install

**Solution**:
- Check `requirements.txt` syntax
- Ensure all package versions are compatible
- Try pinning specific versions
- Check logs for specific package errors

### ❌ File Upload Fails

**Problem**: Can't upload large model file

**Solution**:
- Use Git LFS for files > 100MB
- Split into smaller files (not recommended for models)
- Use Git-based deployment instead

## Updating Your App

### Method 1: Web Interface
1. Go to your Space
2. **"Files and versions"** → **"Add file"**
3. Upload updated file (overwrites existing)
4. Space automatically rebuilds

### Method 2: Git
```bash
# Make changes locally
git add .
git commit -m "Update app"
git push hf main
```

## Custom Domain (Optional)

1. Go to Space settings
2. Scroll to **"Custom domain"**
3. Add your domain
4. Follow DNS configuration instructions

## Sharing Your App

Once deployed, you can:
- Share the public URL
- Embed in websites
- Use API (if enabled)
- Share on social media

## Cost

- **Free tier**: CPU basic, unlimited usage
- **Paid tiers**: Pay per hour of usage
- **Storage**: Generous free storage (perfect for large models)

## Next Steps

1. ✅ Deploy your app
2. ✅ Test with sample images
3. ✅ Share with others
4. ✅ Monitor usage in Space analytics
5. ✅ Upgrade to GPU if needed for faster inference

## Support

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://gradio.app/docs/)
- [Community Forum](https://discuss.huggingface.co/)

---

**Need help?** Check the logs tab in your Space for detailed error messages!
