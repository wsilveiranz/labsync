# Product Requirements Document (PRD) – LabSync

## 1. Vision & Objectives
**Purpose:** Build a minimal, client-side web app for lab resource booking that prevents double-bookings and provides instant availability checking. Focus on core functionality that can be prototyped quickly without backend infrastructure.

**Key Goal:** Create a working prototype in 30-60 minutes that demonstrates the essential booking workflow.

---

## 2. Core User Flows (Priority Order)

### Flow 1: Check Availability (5-10 min to build)
1. User selects a resource from dropdown
2. User picks date/time
3. App shows "Available" or "Booked" status instantly

### Flow 2: Make Booking (10-15 min to build)
1. User fills simple form: Name, Resource, Date, Start Time, Duration
2. App checks for conflicts in real-time
3. App saves booking to localStorage and shows confirmation

### Flow 3: View Bookings (10-15 min to build)
1. User sees list of all current bookings
2. User can filter by resource or date
3. User can delete their own bookings

---

## 3. Minimal Feature Set (Client-Side Only)

### Core Features (Must Have - 30 min)
- **Resource List:** Hardcoded list of 3-5 lab resources
- **Booking Form:** Name, resource dropdown, date picker, time slots
- **Conflict Detection:** Check localStorage for overlapping bookings
- **Booking Storage:** Save/load from browser localStorage
- **Basic Validation:** Prevent past dates, require all fields

### Nice-to-Have (Extra 15-30 min)
- **Visual feedback:** Success/error messages for bookings
- **Delete bookings:** Remove button for each booking
- **Today's schedule:** Quick view of current day's bookings
- **Simple styling:** Basic CSS to make it look professional

### Future Stretch Goals (Post-MVP)
- **Calendar view:** Drag-and-drop booking interface with weekly/monthly views
- **Usage analytics:** Dashboard showing resource utilization patterns
- **Enhanced notifications:** Email alerts for upcoming bookings or conflicts
- **Multi-lab support:** Support for multiple lab environments with role-based access
- **Equipment tracking:** QR code scanning for equipment check-in/check-out
- **Integration capabilities:** Hooks for lab access control or inventory management systems
- **Mobile optimization:** Responsive design optimized for tablets and phones
- **Recurring bookings:** Schedule regular/repeated resource reservations
- **Booking templates:** Save and reuse common booking configurations
- **Advanced conflict resolution:** Suggest alternative times when conflicts occur

---

## 4. Technical Approach (Client-Side Focus)

### Technology Stack
- **Frontend:** Vanilla HTML/CSS/JavaScript (no frameworks needed)
- **Storage:** Browser localStorage for persistence
- **Deployment:** Single HTML file that runs in any browser

### Data Structure (localStorage)
```javascript
// Bookings array stored as JSON
[
  {
    id: "uuid",
    name: "John Doe", 
    resource: "Microscope A",
    date: "2025-09-15",
    startTime: "09:00",
    duration: 120, // minutes
    timestamp: 1694764800000
  }
]
```

### Key Functions to Build
1. `checkConflict(resource, date, startTime, duration)` → boolean
2. `saveBooking(bookingData)` → success/error
3. `getBookings(filterBy)` → array of bookings
4. `deleteBooking(id)` → boolean

---

## 5. Prototype Validation Criteria

### Must Demonstrate (30-45 min mark)
- [x] Can prevent double-booking same resource at same time
- [x] Data persists after browser refresh  
- [x] Form validation prevents invalid inputs
- [x] User can see their booking in the list immediately

### Success Indicators
- **Speed:** Complete core flow (check → book → view) in under 10 clicks
- **Clarity:** Any user can book a resource without instructions
- **Reliability:** Zero double-bookings possible with the conflict detection

---

## 6. Quick Start Implementation Guide

### 30-Minute Version
1. **HTML structure** (5 min): Form + booking list
2. **Basic styling** (5 min): Make it look clean
3. **Core JavaScript** (15 min): Save/load/conflict check
4. **Testing** (5 min): Try to break it with edge cases

### 60-Minute Version (add these)
5. **Enhanced UX** (15 min): Better error messages, loading states
6. **Filtering** (10 min): View bookings by resource or date
7. **Polish** (5 min): Improve styling and responsiveness
