# LabSync Phase 2 - Backend Implementation

Welcome to LabSync Phase 2! This enhanced version adds a Python Flask backend to the original client-side prototype, providing server-side persistence and multi-user support.

## 🚀 What's New in Phase 2

- **Flask Backend API**: RESTful endpoints for resources and bookings
- **Server-side Persistence**: JSON file-based storage that persists across deployments
- **Multi-user Support**: Centralized booking management
- **Data Migration**: Seamless migration from localStorage to server storage
- **Enhanced UI**: Auto-refreshing dashboard with real-time updates
- **Azure Ready**: Configured for deployment to Azure App Service

## 📁 Project Structure

```
src/
├── app.py                   # Flask application with API endpoints
├── requirements.txt         # Python dependencies
├── startup.txt              # Azure App Service startup command
├── templates/
│   └── dashboard.html       # Server-rendered dashboard template
├── static/
│   ├── css/
│   │   └── style.css        # Application styles
│   ├── js/
│   │   └── app.js           # Frontend API integration
│   └── img/
│       └── labsync.png      # LabSync logo
├── data/
│   ├── resources.json       # Available lab resources
│   └── bookings.json        # Booking data storage
├── migration/
│   └── migrate.py           # Data migration utilities
├── index.html               # Phase 1 client-side version (reference)
└── README.md                # This file
```

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Local Development

1. **Navigate to src directory**
   ```powershell
   cd src
   ```

2. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**
   ```powershell
   $env:FLASK_APP="app.py"
   $env:FLASK_ENV="development"
   ```

4. **Run the Application**
   ```powershell
   flask run
   ```
   
   Or use the production server:
   ```powershell
   python app.py
   ```

5. **Access the Application**
   - Open your browser to: http://127.0.0.1:5000
   - The app will automatically create data files on first run

## 🌐 API Endpoints

### Resources
- `GET /api/resources` - List all lab resources
- `GET /api/availability/{resource_id}?date=YYYY-MM-DD` - Check resource availability

### Bookings
- `GET /api/bookings` - List all bookings (supports filtering)
- `POST /api/bookings` - Create a new booking
- `DELETE /api/bookings/{id}` - Delete a booking

### Migration
- `POST /api/migrate` - Migrate localStorage data to server

### Statistics
- `GET /api/stats` - Get booking statistics

### Example API Usage

**Create a Booking:**
```javascript
fetch('/api/bookings', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user: 'John Doe',
    resource_id: 'microscope-a',
    start_time: '2025-09-15T09:00',
    duration: 120
  })
})
```

**Get Today's Bookings:**
```javascript
const today = new Date().toISOString().split('T')[0];
fetch(`/api/bookings?date=${today}`)
```

## 🔄 Data Migration

If you were using the Phase 1 (client-side) version, you can migrate your existing bookings:

1. Open the new backend version in your browser
2. Click the "Migrate localStorage Data" button
3. Your existing bookings will be transferred to the server
4. localStorage data will be automatically cleared after successful migration

## 🚀 Azure Deployment

### Quick Deploy Steps

1. **Create Azure App Service**
   - Runtime: Python 3.x (Linux)
   - Plan: Basic or Free tier for development

2. **Configure App Settings**
   - `WEBSITES_PORT`: 8000 (if needed)
   - `DATA_DIR`: /home/data (for persistent storage)

3. **Deploy the src directory**

   **Option A - GitHub Integration:**
   - Connect your GitHub repository
   - Set the App startup file to: `src/startup.txt`
   - Enable automatic deployments

   **Option B - ZIP Deploy:**
   - Create a ZIP file of the src directory contents
   - Use Azure Portal → Deployment Center → ZIP Deploy

4. **Startup Command**
   ```
   gunicorn app:app --bind=0.0.0.0:8000
   ```

### Environment Variables

For production deployment, consider setting:
- `DATA_DIR`: Path for data storage (default: ./data)
- `FLASK_ENV`: production
- `PORT`: 8000 (for Azure App Service)

## 📊 Features

### Enhanced Booking System
- **Real-time Conflict Detection**: Server-side validation prevents double bookings
- **Persistent Storage**: Bookings survive server restarts and deployments
- **Multi-user Safe**: Centralized storage prevents data conflicts

### Improved User Experience
- **Auto-refresh**: Dashboard updates every 30 seconds
- **Live Statistics**: Real-time resource availability
- **Better Error Handling**: Detailed error messages and retry logic

### Migration Support
- **Backward Compatibility**: Seamless upgrade from Phase 1
- **Data Validation**: Migration process validates and reports issues
- **Conflict Resolution**: Handles overlapping bookings during migration

## 🔧 Technical Details

### Data Storage
- **Format**: JSON files for simplicity and portability
- **Location**: `/data` directory (configurable via DATA_DIR)
- **Persistence**: Files stored in Azure `/home` directory survive deployments

### Security Considerations
- **Input Validation**: All API inputs are validated
- **Error Handling**: Graceful error responses without exposing internals
- **CORS**: Currently open for development (configure for production)

### Performance
- **File-based Storage**: Simple and fast for prototype scale
- **In-memory Caching**: No database overhead
- **Client-side Optimization**: Auto-refresh prevents unnecessary requests

## 🐛 Troubleshooting

### Common Issues

**Flask Import Error:**
```
pip install flask gunicorn
```

**Data Files Not Found:**
- The app automatically creates data files on first run
- Check file permissions in the data directory

**Azure Deployment Issues:**
- Verify startup command: `gunicorn app:app --bind=0.0.0.0:8000`
- Check application logs in Azure Portal
- Ensure requirements.txt includes all dependencies

**Migration Issues:**
- Ensure localStorage contains valid JSON data
- Check browser console for error messages
- Verify localStorage key is 'labsync_bookings'

## � Future Enhancements

Ready for Phase 3? Consider these improvements:
- Database integration (PostgreSQL, MongoDB)
- User authentication and authorization
- Real-time notifications via WebSockets
- Calendar view with drag-and-drop
- Mobile app development
- Advanced analytics and reporting

## 🤝 Contributing

1. Follow the existing code style and structure
2. Test locally before deploying
3. Update documentation for new features
4. Ensure backward compatibility when possible

---

**LabSync Phase 2** - Taking lab resource management to the next level! 🧪⚡