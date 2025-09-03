# 🚀 FitBlendz Pro - Professional Barber Booking System

[![Django](https://img.shields.io/badge/Django-5.2.3-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org/)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Business%20API-green.svg)](https://developers.facebook.com/docs/whatsapp/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, feature-rich barber shop booking system built with Django, featuring WhatsApp integration, interactive dashboard, and advanced appointment management.

## 🌟 **Live Demo**
**🚀 [View Live Application](https://fitblendz-pro.onrender.com)**

## ✨ **Features**

### 🎯 **Core Functionality**
- **📅 Easy Appointment Booking** - Intuitive booking form with real-time availability
- **💼 Service Management** - Manage barber services with pricing and duration
- **🕒 Working Hours** - Configurable working hours and break times
- **🎉 Holiday Management** - Mark holidays and closed dates
- **📊 Status Tracking** - Track appointment status (pending, confirmed, completed, cancelled)

### 📱 **WhatsApp Integration**
- **🔗 Webhook Support** - Properly configured WhatsApp Business API webhook
- **📨 Automatic Notifications** - Send confirmation, reminder, and update messages
- **💬 Interactive Responses** - Handle customer queries via WhatsApp
- **✅ Error-Free Setup** - Resolves common webhook configuration issues
- **🌍 International Support** - Works with Canadian, US, and international numbers

### 👨‍💼 **Admin Dashboard**
- **📊 Interactive Interface** - Modern, responsive admin dashboard
- **⚡ Bulk Actions** - Confirm, complete, or send reminders to multiple appointments
- **🔍 Advanced Filtering** - Filter by status, date, service, and more
- **🔄 Real-time Updates** - AJAX-powered status updates
- **📤 Export Capabilities** - Export appointment data

### 🛡️ **Security & Performance**
- **🔒 Enhanced Security** - CSRF protection, input validation, and secure practices
- **⚡ Optimized Performance** - Database optimization with proper indexing
- **📈 Scalable Architecture** - Clean architecture for easy maintenance and expansion
- **🚦 Rate Limiting** - Protection against spam and abuse
- **🔐 Secure Headers** - XSS protection and content security

## 🛠️ **Technology Stack**

- **Backend**: Django 5.2.3 (Python)
- **Database**: SQLite (development), PostgreSQL (production)
- **Web Server**: Gunicorn (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **WhatsApp API**: Meta WhatsApp Business API v20.0
- **Email**: SMTP integration with Gmail
- **Deployment**: Render.com with automatic SSL

## 📋 **Prerequisites**

- Python 3.8+
- Django 5.2.3
- WhatsApp Business API access
- Gmail account for email notifications
- Git (for deployment)

## 🚀 **Quick Start**

### **1. Clone the Repository**
```bash
git clone https://github.com/Bishkiyaoon/fitblendz-pro.git
cd fitblendz-pro
```

### **2. Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Environment Configuration**
Create a `.env` file in the project root:
```env
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here
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

### **5. Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### **6. Run Development Server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see your application!

## 🌐 **Deployment**

### **Deploy to Render (Recommended)**

1. **Push to GitHub** (see [Deployment Guide](DEPLOYMENT_GUIDE.md))
2. **Connect to Render** - Import from GitHub
3. **Configure Environment Variables** - Set production values
4. **Deploy** - Automatic deployment with PostgreSQL

**Full deployment instructions**: [📖 Deployment Guide](DEPLOYMENT_GUIDE.md)

## 📱 **WhatsApp Setup**

### **1. Get Your Public URL**
Use ngrok for development:
```bash
ngrok http 8000
```

### **2. Configure WhatsApp Business**
- **Callback URL**: `https://your-domain.com/webhook/`
- **Verify Token**: `fitblendz_whatsapp_verify_7c2f4b1e`

### **3. Test the Webhook**
The system includes comprehensive webhook testing and error handling.

## 🎯 **Usage**

### **Customer Booking**
1. Visit the home page
2. Select service and preferred date/time
3. Fill in personal details
4. Receive confirmation via email and WhatsApp

### **Admin Management**
1. Access `/admin-dashboard/`
2. View all appointments with filtering
3. Update statuses and manage bookings
4. Send bulk notifications

### **WhatsApp Commands**
Customers can send these commands via WhatsApp:
- `status` - Check appointment status
- `cancel` - Cancel appointment
- `confirm` - Confirm appointment
- `help` - Show available commands

## 🏗️ **Project Structure**

```
fitblendz_pro/
├── fitblendz_pro/          # Project settings
├── booking/                # Main app
│   ├── models.py          # Database models
│   ├── views.py           # Main views
│   ├── webhook_views.py   # WhatsApp webhook
│   ├── admin.py           # Admin interface
│   ├── utils.py           # Utility functions
│   └── urls.py            # URL routing
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── requirements.txt        # Dependencies
├── render.yaml            # Render deployment config
└── manage.py              # Django management
```

## 🔒 **Security Features**

- CSRF protection on all forms
- Input validation and sanitization
- Secure WhatsApp webhook handling
- Environment variable configuration
- Proper error handling without information leakage
- Rate limiting and security headers

## 📊 **Performance Features**

- **Database Indexes** - Optimized queries with 8+ indexes
- **Query Optimization** - Eliminated N+1 queries
- **Pagination** - 25 items per page for better performance
- **Caching** - Local memory caching configured
- **Connection Pooling** - PostgreSQL connection pooling
- **Performance Monitoring** - Built-in performance analysis tools

## 🧪 **Testing**

### **Performance Testing**
```bash
python performance_monitor.py
```

### **WhatsApp Testing**
```bash
python test_whatsapp_system.py
```

### **Database Migration**
```bash
python migrate_to_postgresql.py
```

## 📈 **Performance Metrics**

- **Page Load Time**: 100-300ms (optimized)
- **Concurrent Users**: 50-100+ (with PostgreSQL)
- **Database Queries**: Optimized with select_related()
- **Security**: Enhanced with rate limiting and security headers

## 🌍 **International Support**

- **Canadian Numbers**: `+1-416-555-1234` ✅
- **US Numbers**: `+1-555-123-4567` ✅
- **International**: Any `+country_code` format ✅
- **WhatsApp**: Automatic formatting for all countries

## 🐛 **Troubleshooting**

### **Common Issues**

1. **WhatsApp Not Working**
   - Check webhook URL is accessible
   - Verify environment variables
   - Test with ngrok first

2. **Email Not Sending**
   - Verify Gmail app password
   - Check SMTP settings
   - Test with simple email

3. **Database Errors**
   - Run migrations: `python manage.py migrate`
   - Check database connection
   - Verify environment variables

### **Debug Commands**
```bash
python manage.py check --deploy
python performance_monitor.py
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- Django framework for the robust backend
- WhatsApp Business API for messaging integration
- Bootstrap for responsive UI components
- Render.com for seamless deployment

## 📞 **Support**

- **Documentation**: [Deployment Guide](DEPLOYMENT_GUIDE.md)
- **Performance**: [Optimization Guide](OPTIMIZATION_GUIDE.md)
- **Issues**: [GitHub Issues](https://github.com/Bishkiyaoon/fitblendz-pro/issues)

---

## 🎉 **Live Demo**

**🚀 [Try FitBlendz Pro Now](https://fitblendz-pro.onrender.com)**

**Your professional barber booking system is ready to use!** ✂️💼

---

<div align="center">
  <strong>Built with ❤️ for barbers worldwide</strong>
</div>