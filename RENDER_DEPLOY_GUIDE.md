# 🚀 Render Deployment Guide for KiranaPro (100% Free)

Follow these simple steps to deploy KiranaPro on Render and get a permanent 24/7 HTTPS URL.

---

### Step 1: Create a Repository on GitHub
1. Go to [GitHub.com](https://github.com) and log in to your account (`bituraja7739-cpu`).
2. Click **New Repository** (green button).
3. Name it: `kirana-store` (keep it Public or Private).
4. Click **Create Repository**.

---

### Step 2: Push your code to GitHub
Open your terminal (PowerShell) and run:

```bash
cd "C:\Users\Asus\.gemini\antigravity\scratch\kirana-store-app"
git branch -M main
git remote add origin https://github.com/bituraja7739-cpu/kirana-store.git
git push -u origin main
```

---

### Step 3: Deploy on Render (Free)
1. Go to [Render.com](https://dashboard.render.com/) and sign up / log in with your GitHub account.
2. Click **New +** &rarr; select **Web Service**.
3. Choose your GitHub repository: `kirana-store`.
4. Fill in the simple details:
   - **Name:** `kirana-store-app` (or any name you like)
   - **Runtime:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python server.py`
   - **Instance Type:** `Free`
5. Click **Create Web Service**.

---

### Step 4: Open and Install on Mobile
Within 1-2 minutes, Render will give you your free live URL:
👉 `https://kirana-store-app.onrender.com`

1. Open this link on your mobile phone in **Google Chrome**.
2. Tap the 3 dots menu `⋮` and tap **"Install App"** / **"Add to Home Screen"**.
3. Android will automatically generate and install the real App on your phone!
4. **Now even if your laptop is completely OFF**, the app will open directly from your phone's memory 24/7!
