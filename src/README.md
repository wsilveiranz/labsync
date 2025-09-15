# LabSync - Lab Resource Booking Application

## 🚀 Quick Start
```bash
# Option 1: Open directly in browser
# Double-click src/index.html

# Option 2: Serve locally
cd src
python -m http.server 8080
# Open http://localhost:8080
```

## ✅ Completed Features

### 1. HTML Structure ✅
- Complete booking form with all required fields
- Resource dropdown with 5 lab resources
- Date and time inputs with proper validation
- Booking list display with filtering options
- Statistics dashboard

### 2. CSS Styling ✅
- **Brand Colors Applied:**
  - Primary: Crimson Red #B91C1C (buttons, headers)
  - Secondary: Warm Coral #F87171 (hover states)  
  - Accent: Golden Amber #F59E0B (highlights)
  - Background: Off-White #F9FAFB
  - Text: Charcoal #111827
- Minimalist design with rounded corners
- Responsive grid layout
- Clean typography and spacing

### 3. Core JavaScript Functions ✅
```javascript
✅ checkConflict(resource, date, startTime, duration) → boolean
✅ saveBooking(bookingData) → {success: boolean, message: string}
✅ getBookings(filterBy) → array of bookings  
✅ deleteBooking(id) → boolean
```

### 4. Conflict Detection Logic ✅
- Time interval overlap algorithm implemented
- Prevents double-bookings for same resource
- Formula: `max(start1, start2) < min(end1, end2)`
- Real-time validation during booking creation

### 5. Form Validation ✅
- **Required field validation** - all fields must be filled
- **Past date prevention** - cannot book resources for past dates
- **Time format validation** - proper time handling
- **User feedback** - success/error alerts with auto-hide
- **Input sanitization** - trim whitespace, validate data types

### 6. Booking Management Features ✅
- **View all bookings** in sorted list (by date/time)
- **Delete bookings** with confirmation dialog
- **Filter by resource** dropdown
- **Filter by date** picker
- **Real-time statistics** showing total bookings, today's bookings, available resources
- **Immediate UI updates** after any action

## 🧪 Testing the Application

### Basic Workflow Test
1. **Fill out booking form:**
   - Enter your name
   - Select a resource (e.g., "Microscope A")
   - Choose today's date
   - Set start time (e.g., "09:00")
   - Select duration (e.g., "2 hours")

2. **Submit booking** - should see success message

3. **Verify booking appears** in the list below

4. **Test conflict detection:**
   - Try booking same resource at overlapping time
   - Should see error message preventing double-booking

5. **Test filtering:**
   - Use resource/date filters to narrow down bookings
   - Verify only matching bookings show

6. **Test deletion:**
   - Click delete button on any booking
   - Confirm deletion in dialog
   - Verify booking disappears from list

### Edge Cases to Test
- [ ] Booking in the past (should be rejected)
- [ ] Empty form submission (should show validation errors)
- [ ] Overlapping time slots (should prevent conflicts)
- [ ] Browser refresh (data should persist)
- [ ] Filter combinations (resource + date)

## 📊 Data Storage
- **Storage:** Browser localStorage
- **Key:** `labsync_bookings`
- **Format:** JSON array of booking objects
- **Persistence:** Survives browser refresh/restart

## 🎯 Validation Criteria Met
- [x] **Conflict Prevention:** Zero double-bookings possible ✅
- [x] **Data Persistence:** Bookings survive browser refresh ✅  
- [x] **Form Validation:** Invalid inputs rejected ✅
- [x] **Immediate Feedback:** Booking appears in list instantly ✅
- [x] **Speed Test:** Complete booking flow in under 10 clicks ✅
- [x] **Usability:** Any user can book without instructions ✅

## 🚀 Next Steps (Future Enhancements)
- Add Flask backend for multi-user support
- Deploy to Azure App Service
- Implement user authentication
- Add calendar view with drag-and-drop
- Email notifications for bookings
- Usage analytics dashboard

## 🏗️ Architecture
- **Phase 1:** Client-side prototype (CURRENT)
- **Phase 2:** Backend enhancement with Flask + Azure (FUTURE)