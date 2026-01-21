# 🚀 Quick Start: Deploy to Hugging Face Spaces

**5-Minute Guide to Get Your App Live**

## ✅ What You Need

- [x] Hugging Face account ([sign up free](https://huggingface.co/join))
- [x] Your model file: `lymphoma_clip_classifier.pth`
- [x] All files in this repository

## ⚠️ Important: Upload Model First!

**Your model is too large for Spaces. Upload it to Models Hub first:**

1. Go to [huggingface.co/new](https://huggingface.co/new)
2. Select **"Model"** (not Space)
3. Name it: `lymphoma-classifier-model`
4. Upload your `lymphoma_clip_classifier.pth` file
5. **Note your repo ID**: `YOUR_USERNAME/lymphoma-classifier-model`

## 📋 Step-by-Step (5 Minutes)

### 1️⃣ Create Space (1 min)

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in:
   - **Name**: `lymphoma-classifier`
   - **SDK**: **Gradio** ⚠️
   - **Hardware**: CPU basic (free)
4. Click **"Create Space"**

### 2️⃣ Upload Files (2 min)

In your Space, go to **"Files and versions"** tab:

**Upload these files:**

1. `app_gradio.py` → Upload as-is
2. `model_utils.py` → Upload as-is  
3. `requirements_hf.txt` → Upload and **rename to `requirements.txt`**
4. `README_HF_SPACES.md` → Upload and **rename to `README.md`**

**⚠️ DO NOT upload the model file!** It's too large. It will download automatically.

**Set Model Repository:**
5. Go to Space settings → **"Variables and secrets"**
6. Add variable:
   - **Key**: `MODEL_REPO_ID`
   - **Value**: `YOUR_USERNAME/lymphoma-classifier-model` (from Step 0)
7. Click **"Save"**

### 3️⃣ Wait for Deployment (2 min)

1. Go to **"Logs"** tab
2. Watch it build (installing packages, loading model...)
3. Wait until you see: `Running on local URL: http://0.0.0.0:7860`

### 4️⃣ Done! 🎉

Your app is live at:
```
https://YOUR_USERNAME-lymphoma-classifier.hf.space
```

## 📁 File Checklist

Before uploading, make sure you have:

- [ ] Model uploaded to Models Hub ✅ (Step 0 - required!)
- [ ] `app_gradio.py` ✅ (created)
- [ ] `model_utils.py` ✅ (exists)
- [ ] `requirements_hf.txt` ✅ (created - rename to `requirements.txt`)
- [ ] `README_HF_SPACES.md` ✅ (created - rename to `README.md`)
- [ ] `MODEL_REPO_ID` environment variable set ✅ (in Space settings)

## ⚠️ Important Notes

1. **Rename files**: `requirements_hf.txt` → `requirements.txt` and `README_HF_SPACES.md` → `README.md`
2. **Model folder**: Create `model/` folder first, then upload the `.pth` file
3. **First deployment**: Takes 5-15 minutes (model download)
4. **Large files**: If model > 100MB, use Git LFS (see detailed guide)

## 🆘 Troubleshooting

**Model not loading?**
- Check model file is in `model/` folder
- Check file name matches exactly
- Look at Logs tab for errors

**Build failing?**
- Check `requirements.txt` syntax
- Verify all files uploaded correctly
- Check Logs for specific errors

## 📚 Need More Help?

See **`HF_SPACES_DEPLOYMENT.md`** for detailed instructions and troubleshooting.

---

**That's it! Your app should be live in ~5 minutes!** 🎊
