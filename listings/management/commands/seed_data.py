"""
Seed command: python manage.py seed_data
Creates demo users and listings for development.
"""
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing

User = get_user_model()

USERS = [
    {"username": "adaeze", "first_name": "Adaeze", "last_name": "Okafor", "email": "adaeze@example.com", "phone": "+2348012345678", "bio": "Software engineer who loves cooking and good music. Very tidy and respectful of shared spaces."},
    {"username": "emeka", "first_name": "Emeka", "last_name": "Nwosu", "email": "emeka@example.com", "phone": "+2348023456789", "bio": "Accountant. Non-smoker, early riser, and I'm usually at work or the gym."},
    {"username": "fatima", "first_name": "Fatima", "last_name": "Bello", "email": "fatima@example.com", "phone": "+2348034567890", "bio": "Pharmacist and part-time blogger. I keep things clean and expect the same from flatmates."},
    {"username": "tunde", "first_name": "Tunde", "last_name": "Adeyemi", "email": "tunde@example.com", "phone": "+2348045678901", "bio": "Marketing manager. Social but know when to give space. I love cooking Nigerian food on weekends."},
    {"username": "ngozi", "first_name": "Ngozi", "last_name": "Eze", "email": "ngozi@example.com", "phone": "+2348056789012", "bio": "Nurse working shifts. Quiet and respectful. Looking for responsible flatmates."},
    {"username": "seun", "first_name": "Seun", "last_name": "Okonkwo", "email": "seun@example.com", "phone": "+2348067890123", "bio": "Product designer working remotely. I have a cat (very friendly!). Very tidy person."},
]

LISTINGS = [
    {
        "host_username": "adaeze",
        "title": "Cozy private room in Lekki Phase 1",
        "description": "Beautiful private room in a 3-bedroom apartment. I'm looking for a working professional or student who is responsible and tidy. The apartment is in a secure estate with 24/7 security and CCTV. We have constant power (inverter + gen) and fast WiFi. Kitchen is shared, fully equipped. The neighbourhood is safe and close to shopping, restaurants and transport.\n\nIdeal flatmate: works or studies, non-smoker, keeps common areas clean, no loud parties.",
        "address": "7 Admiralty Way, Lekki Phase 1",
        "city": "Lagos",
        "state": "Lagos State",
        "room_type": "private",
        "monthly_rent": 120000,
        "security_deposit": 120000,
        "utilities_included": True,
        "current_flatmates": 1,
        "max_flatmates": 2,
        "furnished": "furnished",
        "gender_preference": "female",
        "has_wifi": True, "has_ac": True, "has_security": True, "has_laundry": True,
        "pets_allowed": False, "smoking_allowed": False,
        "available_from": date.today() + timedelta(days=7),
        "status": "available",
    },
    {
        "host_username": "emeka",
        "title": "Spacious shared apartment — 2 rooms available in Ikeja GRA",
        "description": "Two rooms available in a 4-bedroom duplex in Ikeja GRA. Current occupants are 2 male professionals (banker and engineer). Looking for 2 more to complete the house.\n\nThe house has: constant power (prepaid + inverter), fast fibre WiFi, modern kitchen, large living room, clean borehole water, 2 toilets.\n\nPreferably male professionals or postgraduate students. Very quiet and peaceful environment.",
        "address": "15 Isaac John Street, Ikeja GRA",
        "city": "Lagos",
        "state": "Lagos State",
        "room_type": "shared",
        "monthly_rent": 80000,
        "security_deposit": 80000,
        "utilities_included": False,
        "current_flatmates": 2,
        "max_flatmates": 4,
        "furnished": "semi",
        "gender_preference": "male",
        "has_wifi": True, "has_ac": True, "has_parking": True, "has_security": True,
        "pets_allowed": False, "smoking_allowed": False,
        "available_from": date.today() + timedelta(days=14),
        "status": "available",
    },
    {
        "host_username": "fatima",
        "title": "Self-contained studio with all bills included — Wuse 2",
        "description": "Modern studio apartment in the heart of Wuse 2. Perfect for a single professional or student. Everything is included — water, electricity, and WiFi. The studio has a kitchenette and private bathroom.\n\nBuilding has 24/7 security, CCTV, standby generator. 5 minutes walk from Wuse Market and multiple restaurants. Buses and taxis easily accessible.\n\nIdeal for someone who travels frequently or works long hours.",
        "address": "Plot 23, Aminu Kano Crescent, Wuse 2",
        "city": "Abuja",
        "state": "FCT",
        "room_type": "studio",
        "monthly_rent": 150000,
        "security_deposit": 150000,
        "utilities_included": True,
        "current_flatmates": 0,
        "max_flatmates": 1,
        "furnished": "furnished",
        "gender_preference": "any",
        "has_wifi": True, "has_ac": True, "has_security": True,
        "pets_allowed": False, "smoking_allowed": False,
        "available_from": date.today() + timedelta(days=1),
        "status": "available",
    },
    {
        "host_username": "tunde",
        "title": "Entire 3-bedroom apartment for 3 people — Victoria Island",
        "description": "Looking for 2 flatmates to share a beautiful 3-bedroom apartment on Victoria Island. I'll be taking one room and we'd split the rent 3 ways — so each person pays ₦200,000/month.\n\nApartment features: ocean view from the balcony, modern kitchen, large living area, 2 bathrooms, fitted wardrobes in all rooms, underground parking.\n\nLooking for professionals who are clean, quiet, and financially responsible. No drama. Reference required.",
        "address": "8 Ahmadu Bello Way, Victoria Island",
        "city": "Lagos",
        "state": "Lagos State",
        "room_type": "entire",
        "monthly_rent": 200000,
        "security_deposit": 400000,
        "utilities_included": False,
        "current_flatmates": 1,
        "max_flatmates": 3,
        "furnished": "furnished",
        "gender_preference": "any",
        "has_wifi": True, "has_ac": True, "has_parking": True, "has_pool": True, "has_gym": True, "has_security": True,
        "pets_allowed": True, "smoking_allowed": False,
        "available_from": date.today() + timedelta(days=30),
        "status": "available",
    },
    {
        "host_username": "ngozi",
        "title": "Private room in quiet 2-bed flat — Trans Ekulu, Enugu",
        "description": "One room available in my 2-bedroom apartment in Trans Ekulu estate. I'm a nurse so I work shifts — looking for someone independent and quiet.\n\nRoom is fully furnished (bed, wardrobe, desk, AC). We share the kitchen, bathroom, and living room. The apartment is very clean and I intend to keep it that way. Borehole water, inverter power, and satellite TV included.\n\nFemale professionals or postgrad students preferred.",
        "address": "Trans Ekulu Estate, Block 7",
        "city": "Enugu",
        "state": "Enugu State",
        "room_type": "private",
        "monthly_rent": 45000,
        "security_deposit": 45000,
        "utilities_included": True,
        "current_flatmates": 1,
        "max_flatmates": 2,
        "furnished": "furnished",
        "gender_preference": "female",
        "has_wifi": True, "has_ac": True, "has_security": True,
        "pets_allowed": False, "smoking_allowed": False,
        "available_from": date.today() + timedelta(days=5),
        "status": "available",
    },
    {
        "host_username": "seun",
        "title": "Modern room in designer apartment — Yaba",
        "description": "I'm a product designer working from home and I have a beautifully designed apartment in Yaba. One room available for another creative professional.\n\nI do have a very friendly Bengal cat (Mochi) — so must be an animal lover! The apartment is designed beautifully with a great work-from-home setup, super fast WiFi (150Mbps fibre), and a fun creative environment.\n\nLooking for someone in tech, design, or creative industry. Must be cat-friendly, tidy, and cool to hang with.",
        "address": "23 Commercial Avenue, Yaba",
        "city": "Lagos",
        "state": "Lagos State",
        "room_type": "private",
        "monthly_rent": 90000,
        "security_deposit": 90000,
        "utilities_included": True,
        "current_flatmates": 1,
        "max_flatmates": 2,
        "furnished": "furnished",
        "gender_preference": "any",
        "has_wifi": True, "has_ac": True, "has_laundry": True,
        "pets_allowed": True, "smoking_allowed": False,
        "available_from": date.today() + timedelta(days=10),
        "status": "available",
    },
    {
        "host_username": "adaeze",
        "title": "Shared room (female) in 3-bed flat — Jabi, Abuja",
        "description": "Looking for a female to share a room in our friendly 3-bedroom apartment in Jabi. We're currently 3 girls (banker, teacher, student) and looking for a 4th.\n\nThe shared room is spacious with 2 beds and individual wardrobes. Shared bathroom, well-equipped kitchen, nice living room with TV. Close to Jabi Lake Mall, Transcorp Hilton and Apo market.\n\nWe are a fun, drama-free house. Movie nights on weekends!",
        "address": "House 4, Jabi District",
        "city": "Abuja",
        "state": "FCT",
        "room_type": "shared",
        "monthly_rent": 35000,
        "security_deposit": 35000,
        "utilities_included": True,
        "current_flatmates": 3,
        "max_flatmates": 4,
        "furnished": "furnished",
        "gender_preference": "female",
        "has_wifi": True, "has_ac": True, "has_security": True, "has_parking": True,
        "pets_allowed": False, "smoking_allowed": False,
        "available_from": date.today() + timedelta(days=3),
        "status": "available",
    },
    {
        "host_username": "tunde",
        "title": "Executive room in 4-bedroom duplex — Bodija, Ibadan",
        "description": "One executive room available in a well-maintained 4-bedroom duplex in Bodija Estate, Ibadan. The house is close to UI, UCH and Bodija Market.\n\nFeatures: en-suite bathroom, fitted wardrobe, air conditioning, 24/7 borehole water, generator backup, parking. The house is occupied by professionals — no noise, no parties.\n\nOpen to professionals, lecturers, or postgraduate students.",
        "address": "Bodija Estate, Ibadan",
        "city": "Ibadan",
        "state": "Oyo State",
        "room_type": "private",
        "monthly_rent": 40000,
        "security_deposit": 40000,
        "utilities_included": False,
        "current_flatmates": 2,
        "max_flatmates": 4,
        "furnished": "semi",
        "gender_preference": "any",
        "has_wifi": True, "has_ac": True, "has_parking": True, "has_security": True,
        "pets_allowed": False, "smoking_allowed": False,
        "available_from": date.today() + timedelta(days=20),
        "status": "available",
    },
]


class Command(BaseCommand):
    help = 'Seed the database with demo users and listings'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database...')

        # Create admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@flatfinder.com', 'admin123')
            self.stdout.write('✅ Created superuser: admin / admin123')

        # Create demo users
        created_users = {}
        for u in USERS:
            user, created = User.objects.get_or_create(
                username=u['username'],
                defaults={
                    'first_name': u['first_name'],
                    'last_name': u['last_name'],
                    'email': u['email'],
                    'phone': u.get('phone', ''),
                    'bio': u.get('bio', ''),
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'  👤 Created user: {user.username}')
            created_users[u['username']] = user

        # Create listings
        for l in LISTINGS:
            host = created_users.get(l.pop('host_username'))
            if not host:
                continue
            listing, created = Listing.objects.get_or_create(
                host=host,
                title=l['title'],
                defaults={**l, 'views_count': random.randint(5, 200)}
            )
            if created:
                self.stdout.write(f'  🏠 Created listing: {listing.title[:50]}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✨ Done! Seeded {len(USERS)} users and {len(LISTINGS)} listings.\n'
            f'   → Superuser: admin / admin123\n'
            f'   → Demo users: adaeze, emeka, fatima, tunde, ngozi, seun (password: password123)\n'
            f'   → Run: python manage.py runserver\n'
        ))
