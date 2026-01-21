# Deployment Guide

This guide covers deploying the Lymphoma Classification Flask app to various hosting platforms.

## Platform Recommendations

### 🥇 **Railway** (Recommended)
**Best for:** ML apps with large models, easy setup, good free tier
- ✅ Supports large model files
- ✅ Automatic deployments from GitHub
- ✅ Free tier with $5 credit/month
- ✅ Easy environment variable management
- ✅ Supports GPU (paid plans)

**Deployment Steps:**
1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) and sign up
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Flask and deploy
6. Add environment variable: `MODEL_MODE=REAL` (if needed)
7. Your app will be live at `https://your-app-name.up.railway.app`

**Note:** Make sure your `model/lymphoma_clip_classifier.pth` file is committed to Git (or use Railway's volume storage for large files).

---

### 🥈 **Render**
**Best for:** Free tier hosting, easy setup, good documentation
- ✅ Free tier available
- ✅ Automatic SSL certificates
- ✅ Supports large files via disk storage
- ✅ Auto-deploy from GitHub

**Deployment Steps:**
1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --config gunicorn_config.py`
   - **Environment:** Python 3
6. Add environment variable: `MODEL_MODE=REAL`
7. Deploy!

**Note:** For large model files (>100MB), consider using Render's disk storage or hosting the model separately.

---

### 🥇 **Hugging Face Spaces** (Recommended for Large Models)
**Best for:** ML-focused apps, free hosting, supports large model files
- ✅ **FREE hosting** with generous storage (up to 50GB+)
- ✅ **Perfect for large model files** - no size restrictions like Railway
- ✅ Automatic GPU access (on paid plans, CPU free tier available)
- ✅ Great for showcasing ML projects
- ✅ Easy integration with Hugging Face ecosystem
- ✅ Automatic HTTPS and custom domains
- ✅ Public or private spaces

**Deployment Steps (Detailed):**

1. **Prepare your files:**
   - The repository already includes `app_gradio.py` (Gradio interface)
   - Make sure your model file is in `model/lymphoma_clip_classifier.pth`
   - The `requirements_hf.txt` file is ready for Spaces

2. **Create a Hugging Face account:**
   - Go to [huggingface.co](https://huggingface.co)
   - Sign up for a free account
   - Verify your email

3. **Create a new Space:**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Fill in the details:
     - **Space name**: `lymphoma-classifier` (or your preferred name)
     - **SDK**: Select **"Gradio"**
     - **Visibility**: Public (or Private if you prefer)
   - Click "Create Space"

4. **Upload your files:**
   
   **Option A: Using Git (Recommended)**
   ```bash
   # Install Git LFS for large files (if model > 100MB)
   git lfs install
   
   # Add your repository
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   git push hf main
   ```
   
   **Option B: Using Web Interface**
   - In your Space page, click "Files and versions" tab
   - Click "Add file" → "Upload file"
   - Upload these files:
     - `app_gradio.py`
     - `model_utils.py`
     - `requirements_hf.txt` (rename to `requirements.txt` in the upload)
     - `README_HF_SPACES.md` (rename to `README.md` in the upload)
     - `model/lymphoma_clip_classifier.pth` (this may take time if large)
     - `static/` folder contents (CSS, JS if needed)

5. **Configure the Space:**
   - The Space will automatically detect `app_gradio.py` as the main file
   - It will install dependencies from `requirements.txt`
   - The model will load automatically on first run

6. **Wait for deployment:**
   - First deployment takes 5-15 minutes (model download + setup)
   - Subsequent updates are faster
   - Check the "Logs" tab to monitor progress

7. **Your app is live!**
   - Access at: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`
   - Share the link with others!

**Important Notes:**
- **Model File Size**: If your model is very large (>500MB), consider using Git LFS
- **First Load**: The first inference may take longer as the model loads
- **CPU vs GPU**: Free tier uses CPU (slower but works). Upgrade to GPU for faster inference
- **Storage**: Free tier includes generous storage, perfect for large models
- **Custom Domain**: You can add a custom domain in Space settings

**Troubleshooting:**
- If model doesn't load: Check logs in the "Logs" tab
- If out of memory: The free CPU tier has limited RAM, consider upgrading
- If upload fails: Use Git LFS for files > 100MB

---

### **Fly.io**
**Best for:** Global deployment, Docker-based, good performance
- ✅ Free tier with generous limits
- ✅ Global edge deployment
- ✅ Docker-based (more control)
- ✅ Good for production apps

**Deployment Steps:**
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Create `Dockerfile` (see below)
3. Run: `fly launch`
4. Follow the prompts
5. Deploy: `fly deploy`

---

### **Heroku**
**Best for:** Quick deployment, familiar platform
- ⚠️ No longer has free tier
- ✅ Easy setup
- ⚠️ Limited for large ML models
- ✅ Good documentation

**Deployment Steps:**
1. Install Heroku CLI
2. Run: `heroku create your-app-name`
3. Run: `git push heroku main`
4. Set config: `heroku config:set MODEL_MODE=REAL`
5. Open: `heroku open`

---

## Docker Deployment (Universal)

Create a `Dockerfile` for containerized deployment:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Run with gunicorn
CMD ["gunicorn", "app:app", "--config", "gunicorn_config.py", "--bind", "0.0.0.0:8000"]
```

Then build and run:
```bash
docker build -t lymphoma-classifier .
docker run -p 8000:8000 -e MODEL_MODE=REAL lymphoma-classifier
```

---

## Important Considerations

### 1. **Model File Size**
- Your model file (`lymphoma_clip_classifier.pth`) may be large
- Some platforms have file size limits
- **Solutions:**
  - Use Git LFS for large files
  - Host model separately (S3, Google Cloud Storage)
  - Use platform-specific storage (Railway volumes, Render disks)

### 2. **Memory Requirements**
- CLIP models require significant RAM
- **Recommendations:**
  - Use at least 2GB RAM for the app
  - Consider CPU-only PyTorch builds to reduce memory
  - Monitor memory usage in production

### 3. **Environment Variables**
Set these in your hosting platform:
- `MODEL_MODE=REAL` (or `DUMMY` for testing)
- `FLASK_ENV=production` (if needed)

### 4. **Security**
- Don't commit sensitive data
- Use environment variables for secrets
- Consider rate limiting for production
- Add authentication if needed

### 5. **Performance Optimization**
- Model loads at startup (good for Railway/Render)
- Consider caching predictions
- Use CDN for static files
- Monitor response times

---

## Quick Start: Railway (Easiest)

1. **Prepare your repository:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Railway:**
   - Visit [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repo
   - Wait for deployment (5-10 minutes)
   - Your app is live! 🎉

3. **Configure:**
   - Go to "Variables" tab
   - Add `MODEL_MODE=REAL` if needed
   - Redeploy if necessary

---

## Troubleshooting

### Model not loading
- Check model file path is correct
- Verify model file is included in deployment
- Check logs for specific error messages

### Out of memory errors
- Reduce worker count in `gunicorn_config.py`
- Use CPU-only PyTorch: `pip install torch --index-url https://download.pytorch.org/whl/cpu`
- Increase instance memory (upgrade plan)

### Slow inference
- Consider using GPU instances (paid plans)
- Optimize image preprocessing
- Add caching for repeated predictions

---

## Need Help?

- Check platform-specific documentation
- Review application logs in your hosting dashboard
- Test locally first with `gunicorn app:app`
- Monitor resource usage in your hosting platform
