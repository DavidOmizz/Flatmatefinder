from django.db import models
from django.conf import settings
from django.urls import reverse


class Listing(models.Model):
    ROOM_TYPE_CHOICES = [
        ('private', 'Private Room'),
        ('shared', 'Shared Room'),
        ('entire', 'Entire Apartment'),
        ('studio', 'Studio'),
    ]

    GENDER_PREFERENCE_CHOICES = [
        ('any', 'Any Gender'),
        ('male', 'Male Only'),
        ('female', 'Female Only'),
    ]

    FURNISHED_CHOICES = [
        ('furnished', 'Fully Furnished'),
        ('semi', 'Semi Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('taken', 'Taken'),
        ('pending', 'Pending'),
    ]

    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Location
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    # Room details
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='private')
    total_rooms = models.PositiveIntegerField(default=1)
    available_rooms = models.PositiveIntegerField(default=1)
    current_flatmates = models.PositiveIntegerField(default=0)
    max_flatmates = models.PositiveIntegerField(default=2)
    
    # Pricing
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    utilities_included = models.BooleanField(default=False)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Preferences
    furnished = models.CharField(max_length=20, choices=FURNISHED_CHOICES, default='furnished')
    gender_preference = models.CharField(max_length=10, choices=GENDER_PREFERENCE_CHOICES, default='any')
    pets_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)
    
    # Amenities
    has_wifi = models.BooleanField(default=True)
    has_parking = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_laundry = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=True)
    has_security = models.BooleanField(default=False)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    available_from = models.DateField()
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listings:detail', kwargs={'pk': self.pk})

    def get_amenities(self):
        amenities = []
        if self.has_wifi: amenities.append(('WiFi', '📶'))
        if self.has_parking: amenities.append(('Parking', '🚗'))
        if self.has_gym: amenities.append(('Gym', '🏋️'))
        if self.has_pool: amenities.append(('Pool', '🏊'))
        if self.has_laundry: amenities.append(('Laundry', '🧺'))
        if self.has_ac: amenities.append(('Air Conditioning', '❄️'))
        if self.has_security: amenities.append(('Security', '🔒'))
        if self.pets_allowed: amenities.append(('Pets OK', '🐾'))
        return amenities

    @property
    def spots_left(self):
        return self.max_flatmates - self.current_flatmates


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'uploaded_at']

    def __str__(self):
        return f"Image for {self.listing.title}"


class ContactRequest(models.Model):
    """
    Middleman model — all requests go through admin.
    Neither host nor seeker sees each other's contact until admin approves + connects them.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),        # Seeker submitted, admin hasn't acted
        ('reviewing', 'Under Review'),         # Admin is actively handling
        ('connected', 'Connected'),            # Admin has linked both parties
        ('closed', 'Closed'),                  # Deal done or cancelled
        ('declined', 'Declined'),              # Admin declined (bad fit, spam, etc.)
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='contact_requests')
    seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Admin fields — only admin can fill these
    admin_note = models.TextField(blank=True, null=True,
        help_text="Internal note about this request (not shown to users)")
    handled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='handled_requests',
        help_text="Which admin staff member handled this")
    connected_at = models.DateTimeField(null=True, blank=True,
        help_text="When admin made the connection between seeker and host")
    agent_fee_charged = models.DecimalField(max_digits=10, decimal_places=2,
        null=True, blank=True, help_text="Fee collected by platform for this match")
    fee_paid = models.BooleanField(default=False, help_text="Has the agent fee been paid?")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['listing', 'seeker']

    def __str__(self):
        return f"{self.seeker.get_full_name() or self.seeker.username} → {self.listing.title} [{self.get_status_display()}]"

    @property
    def seeker_phone(self):
        return self.seeker.phone or "Not provided"

    @property
    def host_phone(self):
        return self.listing.host.phone or "Not provided"


class AdminActivity(models.Model):
    """Audit trail — every admin action on a request is logged."""
    request = models.ForeignKey(ContactRequest, on_delete=models.CASCADE, related_name='activity_log')
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='admin_activities')
    action = models.CharField(max_length=100)
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.admin_user} — {self.action} at {self.timestamp:%d %b %Y %H:%M}"


class SavedListing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_listings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'listing']

    def __str__(self):
        return f"{self.user} saved {self.listing.title}"
