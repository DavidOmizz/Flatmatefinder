from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Listing, ListingImage, ContactRequest, SavedListing
from .forms import ListingForm, ContactForm, SearchForm


def pings(request):
    return JsonResponse({'message': 'pong'})

def home(request):
    featured = Listing.objects.filter(status='available').order_by('-views_count')[:6]
    latest = Listing.objects.filter(status='available').order_by('-created_at')[:4]
    cities = Listing.objects.filter(status='available').values_list('city', flat=True).distinct()
    total_listings = Listing.objects.filter(status='available').count()
    total_cities = cities.count()
    return render(request, 'listings/home.html', {
        'featured': featured, 'latest': latest,
        'cities': cities, 'total_listings': total_listings, 'total_cities': total_cities,
    })


def listing_list(request):
    listings = Listing.objects.filter(status='available')
    form = SearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data.get('q')
        city = form.cleaned_data.get('city')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        room_type = form.cleaned_data.get('room_type')
        gender_preference = form.cleaned_data.get('gender_preference')
        furnished = form.cleaned_data.get('furnished')
        pets_allowed = form.cleaned_data.get('pets_allowed')
        has_wifi = form.cleaned_data.get('has_wifi')
        has_parking = form.cleaned_data.get('has_parking')
        if q:
            listings = listings.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(city__icontains=q)|Q(address__icontains=q))
        if city: listings = listings.filter(city__icontains=city)
        if min_price: listings = listings.filter(monthly_rent__gte=min_price)
        if max_price: listings = listings.filter(monthly_rent__lte=max_price)
        if room_type: listings = listings.filter(room_type=room_type)
        if gender_preference: listings = listings.filter(gender_preference=gender_preference)
        if furnished: listings = listings.filter(furnished=furnished)
        if pets_allowed: listings = listings.filter(pets_allowed=True)
        if has_wifi: listings = listings.filter(has_wifi=True)
        if has_parking: listings = listings.filter(has_parking=True)
    sort = request.GET.get('sort', '-created_at')
    sort_options = {'price_asc':'monthly_rent','price_desc':'-monthly_rent','newest':'-created_at','popular':'-views_count'}
    listings = listings.order_by(sort_options.get(sort, '-created_at'))
    cities = Listing.objects.values_list('city', flat=True).distinct()
    return render(request, 'listings/list.html', {'listings':listings,'form':form,'cities':cities,'total':listings.count(),'current_sort':sort})


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    listing.views_count += 1
    listing.save(update_fields=['views_count'])
    contact_form = ContactForm()
    user_has_requested = False
    is_saved = False
    if request.user.is_authenticated:
        user_has_requested = ContactRequest.objects.filter(listing=listing, seeker=request.user).exists()
        is_saved = SavedListing.objects.filter(user=request.user, listing=listing).exists()
    if request.method == 'POST' and request.user.is_authenticated:
        if 'contact' in request.POST:
            if user_has_requested:
                messages.warning(request, 'You have already submitted a request for this listing.')
            elif request.user == listing.host:
                messages.error(request, 'You cannot request your own listing.')
            else:
                contact_form = ContactForm(request.POST)
                if contact_form.is_valid():
                    req = contact_form.save(commit=False)
                    req.listing = listing
                    req.seeker = request.user
                    req.save()
                    messages.success(request, '✅ Request submitted! Our team will review it and reach out to you shortly.')
                    return redirect('listings:detail', pk=pk)
    similar = Listing.objects.filter(city=listing.city, status='available').exclude(pk=pk)[:3]
    return render(request, 'listings/detail.html', {
        'listing':listing,'contact_form':contact_form,
        'user_has_requested':user_has_requested,'is_saved':is_saved,'similar':similar,
    })


@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.host = request.user
            listing.save()
            for i, img in enumerate(request.FILES.getlist('images')):
                ListingImage.objects.create(listing=listing, image=img, is_primary=(i==0))
            messages.success(request, 'Listing created successfully! 🎉')
            return redirect('listings:detail', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, 'listings/create.html', {'form': form})


@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, host=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            for img in request.FILES.getlist('images'):
                ListingImage.objects.create(listing=listing, image=img)
            messages.success(request, 'Listing updated!')
            return redirect('listings:detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/edit.html', {'form': form, 'listing': listing})


@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, host=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted.')
        return redirect('accounts:profile')
    return render(request, 'listings/confirm_delete.html', {'listing': listing})


@login_required
def toggle_save(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    saved, created = SavedListing.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        saved.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'saved': created})
    return redirect('listings:detail', pk=pk)


@login_required
def my_requests(request):
    sent = ContactRequest.objects.filter(seeker=request.user).select_related('listing', 'listing__host')
    return render(request, 'listings/my_requests.html', {'sent': sent})


@login_required
def saved_listings(request):
    saved = SavedListing.objects.filter(user=request.user).select_related('listing')
    return render(request, 'listings/saved.html', {'saved': saved})
