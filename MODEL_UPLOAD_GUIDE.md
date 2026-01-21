# 📤 Upload Model to Hugging Face Models Hub

**Step-by-step guide to upload your large model file**

## Why Upload to Models Hub?

- ✅ **No size limit** - Models Hub supports very large files
- ✅ **Free storage** - Unlimited for public models
- ✅ **Automatic download** - Your Space will download it automatically
- ✅ **Version control** - Track different model versions
- ✅ **Sharing** - Easy to share with others

## Quick Steps

### 1. Create Model Repository

1. Go to [huggingface.co/new](https://huggingface.co/new)
2. Select **"Model"** (⚠️ NOT "Space")
3. Fill in:
   - **Model name**: `lymphoma-classifier-model`
   - **Owner**: Your username
   - **Visibility**: 
     - **Public** (recommended - free, unlimited)
     - **Private** (requires Pro plan for large files)
4. Click **"Create model"**

### 2. Upload Model File

1. In your model repository page, click **"Add file"** → **"Upload file"**
2. Select your `lymphoma_clip_classifier.pth` file
3. Wait for upload to complete (may take time for large files)
4. Click **"Commit changes"**

### 3. Note Your Repository ID

Your model repository ID is in the format:
```
YOUR_USERNAME/lymphoma-classifier-model
```

**Example:**
- Username: `johndoe`
- Model name: `lymphoma-classifier-model`
- Repository ID: `johndoe/lymphoma-classifier-model`

**⚠️ Save this ID - you'll need it for your Space!**

## Alternative: Using Git LFS

For very large files (>5GB), use Git LFS:

```bash
# Install Git LFS
git lfs install

# Clone your model repo
git clone https://huggingface.co/YOUR_USERNAME/lymphoma-classifier-model
cd lymphoma-classifier-model

# Track .pth files
git lfs track "*.pth"

# Add and commit
git add .gitattributes
git add lymphoma_clip_classifier.pth
git commit -m "Add model file"
git push
```

## Verify Upload

1. Go to your model repository
2. You should see `lymphoma_clip_classifier.pth` in the file list
3. Check the file size matches your local file

## Next Steps

After uploading your model:

1. ✅ Note your repository ID: `YOUR_USERNAME/lymphoma-classifier-model`
2. ✅ Go to your Space settings
3. ✅ Add environment variable: `MODEL_REPO_ID=YOUR_USERNAME/lymphoma-classifier-model`
4. ✅ Deploy your Space (see QUICK_START_HF.md)

## Troubleshooting

### Upload Fails

**Problem**: Upload times out or fails

**Solutions**:
- Use Git LFS for very large files
- Try uploading during off-peak hours
- Check your internet connection
- Use the Hugging Face CLI: `huggingface-cli upload`

### File Not Found Error

**Problem**: Space can't find the model

**Solutions**:
- Verify repository ID is correct
- Check model file name matches exactly: `lymphoma_clip_classifier.pth`
- Ensure model repository is Public (or add HF token for private)
- Check Space logs for specific error

### Private Model Access

If your model is private:

1. Go to Space settings → **"Variables and secrets"**
2. Add secret:
   - **Key**: `HF_TOKEN`
   - **Value**: Your Hugging Face token (get from [settings](https://huggingface.co/settings/tokens))
3. The code will automatically use this token for authentication

## Using Hugging Face CLI (Advanced)

```bash
# Install CLI
pip install huggingface_hub[cli]

# Login
huggingface-cli login

# Upload file
huggingface-cli upload YOUR_USERNAME/lymphoma-classifier-model \
    lymphoma_clip_classifier.pth \
    lymphoma_clip_classifier.pth
```

## Model Repository Structure

Your model repository should look like:
```
lymphoma-classifier-model/
└── lymphoma_clip_classifier.pth
```

Optional files you can add:
- `README.md` - Model description
- `config.json` - Model configuration
- `tokenizer.json` - If you have a tokenizer

## Security Notes

- **Public models**: Anyone can download (recommended for demos)
- **Private models**: Require authentication token
- **Large files**: Consider compression if possible
- **Versioning**: Use Git tags for model versions

---

**Once uploaded, proceed to Space deployment!** See `QUICK_START_HF.md`
