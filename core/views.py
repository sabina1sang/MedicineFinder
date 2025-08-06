from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm
from .models import User
from django.db.models import Q
from .forms import PharmacyMedicineForm
from .models import Pharmacy
from .forms import SearchForm
import math

#registration view

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # If pharmacy, set is_approved False, else True
            if user.role == 'pharmacy':
                user.is_approved = False
            else:
                user.is_approved = True
            user.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')

            # Redirect based on role
            if user.role == 'pharmacy':
                return redirect('pharmacy_dashboard')
            else:
                return redirect('user_dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


#login view
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.role == 'pharmacy' and not user.is_approved:
                    messages.error(request, 'Your pharmacy account is not approved yet. Please wait for admin approval.')
                    return redirect('login')
                login(request, user)
                messages.success(request, f'Welcome back {user.username}!')
                if user.role == 'pharmacy':
                    return redirect('pharmacy_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def user_dashboard_view(request):
    return render(request, 'user_dashboard.html')

@login_required
def pharmacy_dashboard_view(request):
    return render(request, 'pharmacy_dashboard.html')


def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points in km."""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def search_view(request):
    form = SearchForm(request.GET or None)
    results = PharmacyMedicine.objects.select_related('pharmacy', 'medicine').all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        sort_by = form.cleaned_data.get('sort_by')

        if query:
            results = results.filter(Q(medicine__name__icontains=query))

        # Get lat/lng from request if provided
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')

        if sort_by == 'price':
            results = results.order_by('price')

        elif sort_by == 'distance' and lat and lng:
            try:
                user_lat = float(lat)
                user_lng = float(lng)

                # Attach distance to each result
                results = list(results)  # So we can sort manually
                for pm in results:
                    if hasattr(pm.pharmacy, 'location_lat') and hasattr(pm.pharmacy, 'location_lng'):
                        if pm.pharmacy.location_lat and pm.pharmacy.location_lng:
                            pm.distance = haversine(
                                user_lat, user_lng,
                                pm.pharmacy.location_lat,
                                pm.pharmacy.location_lng
                            )
                        else:
                            pm.distance = None
                    else:
                        pm.distance = None

                # Sort results with distance first, None distances last
                results.sort(key=lambda x: (x.distance is None, x.distance))

            except ValueError:
                pass  # If lat/lng are invalid, skip sorting by distance

    return render(request, 'search.html', {
        'form': form,
        'results': results
    })

def home_view(request):
    return render(request, 'home.html')


@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = PharmacyMedicineForm(request.POST)
        if form.is_valid():
            pharmacy_medicine = form.save(commit=False)

            try:
                # Link the medicine to the pharmacy of the logged-in user
                pharmacy = Pharmacy.objects.get(owner=request.user)
            except Pharmacy.DoesNotExist:
                messages.error(request, "No pharmacy is linked to your account.")
                return redirect('pharmacy_dashboard')  # Or wherever you want

            pharmacy_medicine.pharmacy = pharmacy  # ✅ Assign pharmacy
            pharmacy_medicine.save()
            messages.success(request, "Medicine added successfully!")
            return redirect('pharmacy_dashboard')  # ✅ Redirect after saving
    else:
        form = PharmacyMedicineForm()

    return render(request, 'add_medicine.html', {'form': form})
