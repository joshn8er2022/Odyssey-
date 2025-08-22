# 🚀 Deployment Guide for Content Marketing Agent

## Deploy to Streamlit Community Cloud

### Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in to your account
2. **Click "New Repository"** (green button)
3. **Repository Settings:**
   - Repository name: `content-marketing-agent`
   - Description: `AI-powered content creation assistant for culturally-aware social media marketing`
   - Set to **Public** (required for free Streamlit deployment)
   - ✅ Check "Add a README file"
   - Click **"Create repository"**

### Step 2: Upload Your Code

1. **Download your project** as a ZIP file or use these commands:

```bash
cd /Users/joshisrael/content-marketing-agent
git init
git add .
git commit -m "Initial commit: Content Marketing Agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/content-marketing-agent.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 3: Deploy to Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Fill in the deployment form:**
   - Repository: `YOUR_USERNAME/content-marketing-agent`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: `content-marketing-agent` (or your preferred name)

### Step 4: Add Your API Keys (Secrets)

1. **In the Streamlit Cloud dashboard**, click on your app
2. **Click "Settings"** → **"Secrets"**
3. **Add your secrets** in TOML format:

```toml
OPENAI_API_KEY = "your_openai_api_key_here"

APIFY_API_TOKEN = "your_apify_api_token_here"
```

4. **Click "Save"**

### Step 5: Deploy!

1. **Click "Deploy"** - Streamlit will automatically build and deploy your app
2. **Wait 2-3 minutes** for the build to complete
3. **Your app will be live** at: `https://YOUR_APP_NAME.streamlit.app`

## 🎯 Quick Upload Method (If you prefer manual upload)

If you prefer not to use Git commands:

1. **Create the GitHub repository** (Step 1 above)
2. **Click "uploading an existing file"** on the repository page
3. **Drag and drop all files** from your `content-marketing-agent` folder
4. **Commit the files**
5. **Continue with Step 3** (Deploy to Streamlit Cloud)

## 📁 Files to Include

Make sure these files are in your GitHub repository:

```
content-marketing-agent/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Dependencies
├── README.md             # Documentation
├── .gitignore            # Git ignore file
├── .streamlit/
│   ├── config.toml       # Streamlit config
│   └── secrets.toml.example  # Example secrets
└── src/                  # Source code (optional)
```

## 🔒 Security Notes

- ✅ **Never commit your `.env` file** - it's in `.gitignore`
- ✅ **Use Streamlit Secrets** for API keys in production
- ✅ **Keep your API keys private** - only add them in Streamlit Cloud secrets

## 🎉 After Deployment

Once deployed, you'll have:

- **Public URL**: Share with anyone
- **Automatic updates**: Push to GitHub → Auto-deploys
- **Free hosting**: No cost for public repositories
- **SSL certificate**: Secure HTTPS connection

## 🆘 Troubleshooting

### Common Issues:

1. **"Module not found"**: Check `requirements.txt` has all dependencies
2. **"Secrets not found"**: Make sure API keys are added in Streamlit Cloud secrets
3. **Build fails**: Check the logs in Streamlit Cloud dashboard
4. **App crashes**: Look at the error logs and ensure all imports work

### Getting Help:

- Check Streamlit Community Cloud documentation
- Visit Streamlit Community Forum
- Check GitHub repository issues

Your Content Marketing Agent will be live and accessible to anyone with the URL! 🚀