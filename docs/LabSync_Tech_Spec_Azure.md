# Tech Specification – LabSync Prototype (Azure Deployment)

## 1) Architecture Overview
- **Type:** Client-side first web app with optional backend enhancement
- **Primary Mode:** Single HTML file with localStorage (30-60 min prototype)
- **Enhanced Mode:** Python (Flask) serving a small REST API (optional upgrade)
- **Frontend:** Vanilla HTML/CSS/JavaScript (no frameworks for rapid development)
- **Data Storage:** 
  - **Phase 1:** Browser localStorage (immediate prototyping)
  - **Phase 2:** Local JSON files via Flask backend (persistence upgrade)
- **Deployment:** 
  - **Phase 1:** Static hosting (any web server, GitHub Pages)
  - **Phase 2:** Azure App Service (Linux, Python runtime)

---

## 2) Tech Stack

**Phase 1: Rapid Prototype (30-60 min)**
- **Frontend Only:** HTML5, CSS3, Vanilla JavaScript
- **Storage:** Browser localStorage
- **Deployment:** Single HTML file (any static hosting)

**Phase 2: Enhanced Version (Optional Backend)**
- **Backend:** Python 3.x + Flask + Gunicorn
- **Frontend:** Same as Phase 1
- **Storage:** JSON files + localStorage sync
- **Deployment:** Azure App Service (Linux, Python 3.x)
- **CI/CD:** GitHub Actions or manual ZIP deploy

**Styling Approach**
- **Brand Identity:** LabSync - "Smart Scheduling for Smarter Science"
- **Color Palette:**
  - Primary: Crimson Red `#B91C1C` (buttons, headers, key actions)
  - Secondary: Warm Coral `#F87171` (hover states, secondary elements)
  - Accent: Golden Amber `#F59E0B` (highlights, success states)
  - Background: Off-White `#F9FAFB` (page background)
  - Text: Charcoal `#111827` (high contrast, WCAG compliant)
- **Design Philosophy:** Minimalist and modern with clean lines, rounded corners, and subtle shadows
- **Typography:** Bold sans-serif for headings, vibrant red accents for key actions
- **Layout:** Light and airy with plenty of white space
- **Implementation:** Minimal CSS for rapid development, Optional: Tailwind CSS for polish phase

---

## 3) Data Model

### Phase 1: localStorage Structure (Client-Side)
```javascript
// localStorage keys:
// 'labsync_resources' - hardcoded resource list
// 'labsync_bookings' - all bookings array

// Resources (hardcoded in JS for prototype)
const RESOURCES = [
  { id: "microscope-a", name: "Microscope A", type: "equipment" },
  { id: "microscope-b", name: "Microscope B", type: "equipment" },
  { id: "cold-room-1", name: "Cold Room 1", type: "room" },
  { id: "centrifuge", name: "Centrifuge", type: "equipment" },
  { id: "pcr-machine", name: "PCR Machine", type: "equipment" }
];

// Bookings array (matches PRD specification)
[
  {
    id: "uuid-string",
    name: "John Doe",
    resource: "Microscope A",
    date: "2025-09-15",
    startTime: "09:00",
    duration: 120, // minutes
    timestamp: 1694764800000
  }
]
```

### Phase 2: JSON Files (Backend Enhancement)
```json
// resources.json
[
  { "id": "microscope-a", "name": "Microscope A", "type": "equipment", "status": "available" },
  { "id": "cold-room-1", "name": "Cold Room 1", "type": "room", "status": "available" }
]

// bookings.json (converted from localStorage format)
[
  {
    "id": "uuid-string",
    "resource_id": "microscope-a",
    "user": "John Doe",
    "start_time": "2025-09-15T09:00",
    "end_time": "2025-09-15T11:00",
    "timestamp": 1694764800000
  }
]
```

---

## 4) Core Functions & API Design

### Phase 1: Client-Side Functions (Priority Implementation)
```javascript
// Core functions matching PRD requirements
function checkConflict(resource, date, startTime, duration) {
  // Check localStorage for overlapping bookings
  // Returns boolean
}

function saveBooking(bookingData) {
  // Validate, check conflicts, save to localStorage
  // Returns {success: boolean, message: string}
}

function getBookings(filterBy = {}) {
  // Retrieve from localStorage with optional filtering
  // Returns array of bookings
}

function deleteBooking(id) {
  // Remove booking from localStorage
  // Returns boolean
}
```

### Phase 2: API Endpoints (Backend Enhancement)
- `GET /resources` → List all resources
- `GET /bookings` → List all bookings
- `POST /bookings` → Create booking (conflict check + save)
- `DELETE /bookings/<id>` → Remove booking
- `GET /availability/<resource_id>?date=YYYY-MM-DD` → Day availability

**Conflict Detection Logic:**
Two bookings overlap if `max(start1, start2) < min(end1, end2)`

**Time Handling:**
- Phase 1: Date strings + time strings ("09:00") + duration minutes
- Phase 2: ISO timestamps for backend compatibility

---

## 5) Implementation Strategy

### Phase 1: 30-60 Minute Prototype
1. **Single HTML file** with embedded CSS/JS
2. **Hardcoded resources** in JavaScript array
3. **localStorage persistence** - no server needed
4. **Simple time handling** - date strings + time strings
5. **Immediate deployment** - works in any browser

### Implementation Sequence (matches PRD flows)
1. **Resource dropdown + date picker** (5-10 min)
2. **Booking form + conflict detection** (10-15 min)
3. **Booking list + delete functionality** (10-15 min)
4. **Basic styling + validation** (10-15 min)

### Phase 2: Backend Enhancement (Optional)
- **Migrate localStorage to Flask backend**
- **Add multi-user support** 
- **Implement proper authentication**
- **Deploy to Azure App Service**

---

## 6) Azure Deployment Steps (Quick Path)
1. **Create App Service**
   - Runtime stack: **Python 3.x** (Linux)
   - Choose a Basic/Free plan for prototype
2. **Project Files**
   - `requirements.txt` must include: `flask`, `gunicorn`
   - Startup command: `gunicorn app:app --bind=0.0.0.0:8000`
3. **Deploy**
   - **Option A – GitHub**: Connect repo in App Service → enable build/deploy
   - **Option B – ZIP Deploy**: `Azure Portal → Deployment Center → Zip` (upload your project)
4. **App Settings** (Configuration)
   - (If needed) `WEBSITES_PORT=8000`
   - (Optional) `DATA_DIR=/home/data` and store JSON there for persistence across deployments
5. **Persisting JSON**
   - Files in `/home` are persisted across restarts. If you store JSON **inside** the deployed app folder, they may be overwritten on redeploy. Prefer `/home/data` and point the app to it via `DATA_DIR`.
6. **Test**
   - Open the App Service URL and exercise the endpoints/UI

---

## 7) Success Metrics

### Phase 1 Validation (30-45 min mark)
- [x] **Conflict Prevention:** Zero double-bookings possible
- [x] **Data Persistence:** Bookings survive browser refresh
- [x] **Form Validation:** Invalid inputs rejected
- [x] **Immediate Feedback:** Booking appears in list instantly
- [x] **Speed Test:** Complete booking flow in under 10 clicks
- [x] **Usability:** Any user can book without instructions

### Phase 2 Validation (Backend)
- App deployable to Azure without errors
- Multi-user booking conflicts prevented
- Data migration from localStorage works
- Backend persistence across deployments

---

## 8) Constraints & Assumptions
- **No database**; all persistence via JSON files
- **Basic auth** only (username + role lookup; no OAuth/SSO)
- **Single-instance** App Service (no concurrency or scale-out handling)
- **Workshop goal:** simple, buildable quickly; not production-hardened

---

## 9) Folder Structure

### Phase 1: Client-Side Prototype
```
labsync/
├─ index.html            # Complete prototype in single file
├─ README.md             # Setup instructions
└─ docs/                 # PRD and tech specs
```

### Phase 2: Backend Enhancement
```
labsync/
├─ index.html            # Client-side prototype (reference)
├─ app.py                # Flask app with localStorage migration
├─ requirements.txt      # flask, gunicorn
├─ static/               # css/js assets (extracted from index.html)
├─ templates/            # server-rendered dashboard
├─ data/                 # resources.json, bookings.json
├─ migration/            # localStorage to backend migration scripts
└─ docs/                 # documentation
```

---

## 10) Development & Deployment

### Phase 1: Instant Prototype
```bash
# No setup required - just open in browser
open index.html
# OR serve locally
python -m http.server 8000  # Navigate to localhost:8000
```

### Phase 2: Backend Development
```bash
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP="app.py"
$env:FLASK_ENV="development"
flask run  # http://127.0.0.1:5000
```

**Azure Production:**
```bash
gunicorn app:app --bind=0.0.0.0:8000
```

---

## 11) Notes & Next Steps (Stretch)
- Add calendar view (drag & drop)
- Add notifications (email/in-app)
- Add analytics (resource utilization)
- Consider moving to a lightweight DB (e.g., SQLite/Azure Files) when collaboration grows
