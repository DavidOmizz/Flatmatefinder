from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from listings.models import Listing, ContactRequest, AdminActivity
from accounts.models import User


def is_staff(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_staff, login_url='/')
def dashboard_home(request):
    now = timezone.now()
    last_7 = now - timedelta(days=7)
    last_30 = now - timedelta(days=30)

    stats = {
        'total_requests': ContactRequest.objects.count(),
        'pending_requests': ContactRequest.objects.filter(status='pending').count(),
        'reviewing_requests': ContactRequest.objects.filter(status='reviewing').count(),
        'connected_requests': ContactRequest.objects.filter(status='connected').count(),
        'total_listings': Listing.objects.count(),
        'active_listings': Listing.objects.filter(status='available').count(),
        'total_users': User.objects.filter(is_staff=False).count(),
        'new_users_7d': User.objects.filter(created_at__gte=last_7, is_staff=False).count(),
        'new_requests_7d': ContactRequest.objects.filter(created_at__gte=last_7).count(),
        'new_requests_30d': ContactRequest.objects.filter(created_at__gte=last_30).count(),
        'fees_collected': ContactRequest.objects.filter(fee_paid=True).aggregate(total=Sum('agent_fee_charged'))['total'] or 0,
        'fees_pending': ContactRequest.objects.filter(status='connected', fee_paid=False).aggregate(total=Sum('agent_fee_charged'))['total'] or 0,
    }

    # Latest pending requests — these need action
    urgent = ContactRequest.objects.filter(
        status__in=['pending', 'reviewing']
    ).select_related('seeker', 'listing', 'listing__host').order_by('-created_at')[:10]

    # Recent connections made
    recent_connections = ContactRequest.objects.filter(
        status='connected'
    ).select_related('seeker', 'listing', 'listing__host').order_by('-connected_at')[:5]

    # Most requested listings
    hot_listings = Listing.objects.annotate(
        req_count=Count('contact_requests')
    ).order_by('-req_count')[:5]

    return render(request, 'dashboard/home.html', {
        'stats': stats,
        'urgent': urgent,
        'recent_connections': recent_connections,
        'hot_listings': hot_listings,
    })


@login_required
@user_passes_test(is_staff, login_url='/')
def request_list(request):
    requests = ContactRequest.objects.select_related(
        'seeker', 'listing', 'listing__host', 'handled_by'
    )

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        requests = requests.filter(status=status_filter)

    # Search
    q = request.GET.get('q', '')
    if q:
        requests = requests.filter(
            Q(seeker__first_name__icontains=q) |
            Q(seeker__last_name__icontains=q) |
            Q(seeker__username__icontains=q) |
            Q(listing__title__icontains=q) |
            Q(listing__city__icontains=q) |
            Q(listing__host__first_name__icontains=q)
        )

    requests = requests.order_by('-created_at')

    status_counts = {
        'all': ContactRequest.objects.count(),
        'pending': ContactRequest.objects.filter(status='pending').count(),
        'reviewing': ContactRequest.objects.filter(status='reviewing').count(),
        'connected': ContactRequest.objects.filter(status='connected').count(),
        'closed': ContactRequest.objects.filter(status='closed').count(),
        'declined': ContactRequest.objects.filter(status='declined').count(),
    }

    return render(request, 'dashboard/requests.html', {
        'requests': requests,
        'status_filter': status_filter,
        'status_counts': status_counts,
        'search_q': q,
    })


@login_required
@user_passes_test(is_staff, login_url='/')
def request_detail(request, pk):
    req = get_object_or_404(
        ContactRequest.objects.select_related('seeker', 'listing', 'listing__host', 'handled_by'),
        pk=pk
    )
    activity_log = req.activity_log.select_related('admin_user').all()

    if request.method == 'POST':
        action = request.POST.get('action')
        note = request.POST.get('note', '')
        fee = request.POST.get('agent_fee_charged', '')

        old_status = req.status

        if action == 'start_review':
            req.status = 'reviewing'
            req.handled_by = request.user
            req.save()
            AdminActivity.objects.create(request=req, admin_user=request.user, action='Started review', note=note)
            messages.success(request, f'Request marked as Under Review.')

        elif action == 'connect':
            req.status = 'connected'
            req.handled_by = request.user
            req.connected_at = timezone.now()
            if fee:
                req.agent_fee_charged = fee
            if note:
                req.admin_note = note
            req.save()
            AdminActivity.objects.create(
                request=req, admin_user=request.user,
                action='Connected seeker and host',
                note=f"Fee: ₦{fee or 0}. {note}"
            )
            messages.success(request, f'✅ Connected! {req.seeker.get_full_name()} ↔ {req.listing.host.get_full_name()}. Remember to share contacts with both parties.')

        elif action == 'mark_fee_paid':
            req.fee_paid = True
            req.save()
            AdminActivity.objects.create(request=req, admin_user=request.user, action='Marked fee as paid', note=note)
            messages.success(request, 'Fee marked as paid.')

        elif action == 'close':
            req.status = 'closed'
            req.save()
            AdminActivity.objects.create(request=req, admin_user=request.user, action='Closed request', note=note)
            messages.info(request, 'Request closed.')

        elif action == 'decline':
            req.status = 'declined'
            req.save()
            AdminActivity.objects.create(request=req, admin_user=request.user, action='Declined request', note=note)
            messages.warning(request, 'Request declined.')

        elif action == 'add_note':
            req.admin_note = note
            req.save()
            AdminActivity.objects.create(request=req, admin_user=request.user, action='Added note', note=note)
            messages.success(request, 'Note saved.')

        return redirect('dashboard:request_detail', pk=pk)

    return render(request, 'dashboard/request_detail.html', {
        'req': req,
        'activity_log': activity_log,
    })


@login_required
@user_passes_test(is_staff, login_url='/')
def listings_overview(request):
    listings = Listing.objects.annotate(
        req_count=Count('contact_requests'),
        pending_count=Count('contact_requests', filter=Q(contact_requests__status='pending')),
    ).select_related('host').order_by('-created_at')

    status_filter = request.GET.get('status', '')
    if status_filter:
        listings = listings.filter(status=status_filter)

    return render(request, 'dashboard/listings.html', {'listings': listings, 'status_filter': status_filter})


@login_required
@user_passes_test(is_staff, login_url='/')
def users_overview(request):
    users = User.objects.filter(is_staff=False).annotate(
        listing_count=Count('listings'),
        request_count=Count('sent_requests'),
    ).order_by('-created_at')
    return render(request, 'dashboard/users.html', {'users': users})
