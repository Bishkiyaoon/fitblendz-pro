# 🚀 FitBlendz Pro - Deployment Guide

## **GitHub & Render Deployment Instructions**

### **Prerequisites**
1. **Git** - Install from [git-scm.com](https://git-scm.com/)
2. **GitHub Account** - Sign up at [github.com](https://github.com/)
3. **Render Account** - Sign up at [render.com](https://render.com/)

---

## **📁 Step 1: Install Git (if not installed)**

### **Windows:**
1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer with default settings
3. Restart your terminal/command prompt

### **Verify Installation:**
```bash
git --version
```

---

## **🔧 Step 2: Configure Git (First time only)**

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## **📤 Step 3: Push to GitHub**

### **3.1 Initialize Repository:**
```bash
git init
git add .
git commit -m "Initial commit: FitBlendz Pro with optimizations"
```

### **3.2 Create GitHub Repository:**
1. Go to [github.com](https://github.com/)
2. Click "New repository"
3. Name: `fitblendz-pro`
4. Description: `Professional Barber Booking System with WhatsApp Integration`
5. Make it **Public** (required for free Render deployment)
6. **Don't** initialize with README (we already have files)
7. Click "Create repository"

### **3.3 Push to GitHub:**
```bash
git remote add origin https://github.com/Bishkiyaoon/fitblendz-pro.git
git branch -M main
git push -u origin main
```

---

## **🌐 Step 4: Deploy to Render**

### **4.1 Create Render Account:**
1. Go to [render.com](https://render.com/)
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

### **4.2 Create Web Service:**
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `fitblendz-pro`
3. Configure the service:

**Basic Settings:**
- **Name**: `fitblendz-pro`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3.11.0`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements-prod.txt && python manage.py migrate`
- **Start Command**: `gunicorn fitblendz_pro.wsgi:application`

### **4.3 Create PostgreSQL Database:**
1. Click "New +" → "PostgreSQL"
2. Name: `fitblendz-postgres`
3. Plan: **Free**
4. Click "Create Database"
5. Copy the **External Database URL**

### **4.4 Configure Environment Variables:**

In your Render web service, go to "Environment" tab and add:

```env
DEBUG=False
DJANGO_SECRET_KEY=your-very-secure-secret-key-here
ALLOWED_HOSTS=fitblendz-pro.onrender.com
DATABASE_URL=postgresql://user:password@host:port/database
WHATSAPP_TOKEN=your-whatsapp-token
PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_VERIFY_TOKEN=your-verify-token
BARBER_WHATSAPP=+916239514954
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### **4.5 Update Database Settings:**

Replace the `DATABASE_URL` in your environment variables with the PostgreSQL URL from step 4.3.

---

## **🔧 Step 5: Update Settings for Production**

### **5.1 Update settings.py:**
The settings are already configured to use PostgreSQL in production mode.

### **5.2 Update render.yaml:**
Update the `DB_HOST` in `render.yaml` with your actual PostgreSQL host.

---

## **🚀 Step 6: Deploy**

1. Click "Create Web Service" in Render
2. Wait for deployment (5-10 minutes)
3. Your app will be available at: `https://fitblendz-pro.onrender.com`

---

## **📱 Step 7: Configure WhatsApp Webhook**

### **7.1 Update Webhook URL:**
In your WhatsApp Business API settings:
- **Callback URL**: `https://fitblendz-pro.onrender.com/webhook/`
- **Verify Token**: `fitblendz_whatsapp_verify_7c2f4b1e`

### **7.2 Test Webhook:**
1. Go to your deployed app
2. Create a test appointment
3. Check if WhatsApp notifications work

---

## **🔍 Step 8: Testing & Verification**

### **8.1 Test Basic Functionality:**
- [ ] Home page loads
- [ ] Booking form works
- [ ] Admin dashboard accessible
- [ ] Database operations work

### **8.2 Test WhatsApp Integration:**
- [ ] Appointment notifications sent
- [ ] Barber approval requests work
- [ ] Customer commands work

### **8.3 Test Email Integration:**
- [ ] Confirmation emails sent
- [ ] Status update emails work

---

## **🛠️ Troubleshooting**

### **Common Issues:**

**1. Build Fails:**
- Check `requirements-prod.txt` for all dependencies
- Ensure Python version compatibility

**2. Database Connection Error:**
- Verify `DATABASE_URL` is correct
- Check PostgreSQL service is running

**3. WhatsApp Not Working:**
- Verify webhook URL is accessible
- Check environment variables are set
- Test webhook with ngrok first

**4. Email Not Working:**
- Verify Gmail app password
- Check SMTP settings
- Test with a simple email first

### **Debug Commands:**
```bash
# Check logs in Render dashboard
# Test locally with production settings
python manage.py check --deploy
```

---

## **📊 Performance Monitoring**

### **Render Dashboard:**
- Monitor CPU and memory usage
- Check response times
- View error logs

### **Application Monitoring:**
```bash
# Run performance monitor
python performance_monitor.py
```

---

## **🔒 Security Checklist**

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] Environment variables secured
- [ ] HTTPS enabled (automatic on Render)
- [ ] Database credentials protected

---

## **🎉 Success!**

Your FitBlendz Pro application is now live at:
**https://fitblendz-pro.onrender.com**

### **Next Steps:**
1. **Custom Domain** (optional): Connect your own domain
2. **SSL Certificate** (automatic on Render)
3. **Monitoring**: Set up error tracking
4. **Backups**: Configure database backups
5. **Scaling**: Upgrade to paid plan for better performance

---

## **📞 Support**

If you encounter issues:
1. Check Render logs in dashboard
2. Verify all environment variables
3. Test locally with production settings
4. Check WhatsApp Business API status

**Your professional barber booking system is now live! 🚀**
