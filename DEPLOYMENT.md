# Deployment Guide - App Tester

## 🚀 Frontend on Vercel (Recommended)

### Quick Deploy (2 minutes)

1. Go to **https://vercel.com/dashboard**
2. Click **"Add New"** → **"Project"**
3. Select **"Import Git Repository"**
4. Choose **`Jabir-Srj/app-tester`**
5. Configure:
   - **Framework Preset:** Vite
   - **Build Command:** `cd frontend && npm run build`
   - **Output Directory:** `frontend/dist`
   - **Root Directory:** Leave blank
6. Click **"Deploy"**

**Result:** Your frontend will be live at `https://app-tester.vercel.app` (or similar)

---

## 🔌 Backend Deployment Options

### Option 1: Railway.app (Recommended - Easiest)

1. Go to **https://railway.app**
2. Click **"New Project"** → **"Deploy from GitHub"**
3. Select **`Jabir-Srj/app-tester`**
4. In settings:
   - **Service Name:** app-tester-backend
   - **Environment:** Python 3.11
   - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app`
5. Add environment variables (if needed)
6. Deploy

**Backend URL:** Copy from Railway dashboard, use in frontend config

---

### Option 2: Render.com

1. Go to **https://render.com**
2. Create **"New Web Service"**
3. Connect GitHub repo
4. Configure:
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app`
5. Set environment variables
6. Deploy

---

## 🔗 Connect Frontend to Backend

After deploying backend, update frontend:

Create `.env.production` in `frontend/`:
```
VITE_API_URL=https://your-backend-url.app
```

Update `frontend/src/App.tsx` axios config:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
});
```

---

## 📊 Deployment Summary

| Service | Component | Cost | Deploy Time |
|---------|-----------|------|------------|
| Vercel | Frontend (Vite) | Free | 1-2 min |
| Railway | Backend (Python) | Free tier | 2-3 min |
| Total | Full Stack | Free | ~5 min |

---

## ✅ After Deployment

1. Frontend live at `https://app-tester.vercel.app`
2. Backend API at `https://your-backend.railway.app`
3. Users can upload code and scan it live
4. No local setup needed - it's all cloud-hosted

---

## 🔧 Environment Variables (Backend)

If deploying backend, set these in Railway/Render dashboard:
```
FLASK_ENV=production
DATABASE_URL=sqlite:///app_tester.db
SECRET_KEY=your-secret-key-here
```

---

**All set for cloud deployment!** ☁️
