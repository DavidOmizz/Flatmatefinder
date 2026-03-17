# 🏠 FlatFinder — Flatmate & Room Sharing MVP

A full-featured Django web app for connecting people who want to share apartments and split rent.

## Features

- **Browse Listings** — Search by city, price, room type, furnishing, gender preference, amenities
- **Post a Listing** — Upload photos, set price, describe your space and ideal flatmate
- **Contact Host** — Send a message/request to the host; hosts can accept or decline
- **Save Listings** — Save favourites for later
- **User Profiles** — Manage your listings and view all your requests in one place
- **Seeded Demo Data** — 6 demo users with 8 realistic Nigerian listings across Lagos, Abuja, Enugu, Ibadan

---

## Quick Start

### 1. Install dependencies
```bash
pip install django pillow
```

### 2. Run migrations
```bash
cd flatmate_finder
python manage.py migrate
```

### 3. Seed demo data
```bash
python manage.py seed_data
```

### 4. Start the server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## Demo Accounts

| Username | Password | Name |
|----------|----------|------|
| admin | admin123 | Admin (superuser) |
| adaeze | password123 | Adaeze Okafor |
| emeka | password123 | Emeka Nwosu |
| fatima | password123 | Fatima Bello |
| tunde | password123 | Tunde Adeyemi |
| ngozi | password123 | Ngozi Eze |
| seun | password123 | Seun Okonkwo |

Admin panel: **http://127.0.0.1:8000/admin**

---

## Project Structure

```
flatmate_finder/
├── manage.py
├── requirements.txt
├── flatmate_finder/        # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── listings/               # Main app
│   ├── models.py           # Listing, ListingImage, ContactRequest, SavedListing
│   ├── views.py            # All views (home, list, detail, create, edit, delete, etc.)
│   ├── forms.py            # ListingForm, ContactForm, SearchForm
│   ├── urls.py
│   └── management/commands/seed_data.py
├── accounts/               # Auth app
│   ├── models.py           # Custom User model
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── templates/              # All HTML templates
│   ├── base.html
│   ├── listings/
│   │   ├── home.html
│   │   ├── list.html
│   │   ├── detail.html
│   │   ├── create.html
│   │   ├── edit.html
│   │   ├── requests.html
│   │   ├── saved.html
│   │   └── confirm_delete.html
│   └── accounts/
│       ├── login.html
│       ├── register.html
│       └── profile.html
└── media/                  # Uploaded images (auto-created)
```

---

## Data Models

### Listing
- Title, description, address, city, state
- Room type (private/shared/entire/studio)
- Monthly rent, security deposit, utilities included
- Max flatmates, current flatmates (auto-calculates spots left)
- Gender preference, furnished status
- Amenities: WiFi, AC, parking, gym, pool, laundry, security
- Rules: pets allowed, smoking allowed
- Status: available / taken / pending

### User (extends AbstractUser)
- Phone, bio, avatar
- Related listings, sent requests, saved listings

### ContactRequest
- Sender → Listing
- Message text
- Status: pending / accepted / declined

### SavedListing
- User → Listing bookmark

---

## Next Steps / Roadmap

- [ ] Pagination for listing results
- [ ] Email notifications when a request is accepted/declined
- [ ] Map integration (Google Maps / Leaflet)
- [ ] Listing verification / featured listings
- [ ] In-app messaging thread (beyond single contact request)
- [ ] Listing expiry / auto-delist after N days
- [ ] Payment integration for premium listings
- [ ] Mobile app (React Native)
