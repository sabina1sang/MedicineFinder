from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime
from rest_framework import generics
from .models import Pharmacy
from .serializers import PharmacySerializer
import math

from .forms import (
    UserRegisterForm, UserLoginForm,
    PharmacyMedicineForm, MedicineForm,
    SearchForm, PharmacyLocationForm
)
from .models import User, Pharmacy, PharmacyMedicine, Medicine


# =========================
# REGISTRATION
# =========================
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
             # Set the password properly (hash it)
            raw_password = form.cleaned_data.get('password1')  # or whatever your password field is
            user.set_password(raw_password)  # <-- This hashes the password


            # Set approval flag based on role
            if user.role == 'pharmacy':
                user.is_approved = False
            else:
                user.is_approved = True

            user.save()
            print(f"User saved with role: {user.role}, username: {user.username}")

            # Create Pharmacy if user is pharmacy owner
            if user.role == 'pharmacy':
                pharmacy = Pharmacy.objects.create(owner=user, name=f"{user.username}'s Pharmacy", address='', phone='')
                print(f"Created pharmacy: {pharmacy}")

            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')

            # Redirect based on role
            if user.role == 'pharmacy':
                return redirect('pharmacy_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            print("Form is invalid:", form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


# =========================
# LOGIN
# =========================
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
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


# =========================
# DASHBOARDS
# =========================
@login_required
def user_dashboard_view(request):
    return render(request, 'user_dashboard.html')


@login_required
def pharmacy_dashboard_view(request):
    return render(request, 'pharmacy_dashboard.html')


@login_required
def dashboard_redirect(request):
    return redirect('pharmacy_dashboard' if request.user.role == 'pharmacy' else 'user_dashboard')


# =========================
# LOCATION UPDATE
# =========================
@login_required
def update_pharmacy_location(request):
    if request.user.role != 'pharmacy':
        messages.error(request, "Only pharmacy owners can update location.")
        return redirect('dashboard_redirect')

    pharmacy = get_object_or_404(Pharmacy, owner=request.user)

    if request.method == 'POST':
        form = PharmacyLocationForm(request.POST, instance=pharmacy)
        if form.is_valid():
            form.save()
            messages.success(request, "Pharmacy location updated successfully!")
            return redirect('pharmacy_dashboard')
    else:
        form = PharmacyLocationForm(instance=pharmacy)

    return render(request, 'update_pharmacy_location.html', {'form': form})


# =========================
# MAP API
# =========================
def pharmacy_locations_api(request):
    pharmacies = Pharmacy.objects.exclude(latitude__isnull=True, longitude__isnull=True)
    data = [
        {
            'name': p.name,
            'lat': p.latitude,
            'lng': p.longitude,
            'address': p.address,
        } for p in pharmacies
    ]
    return JsonResponse(data, safe=False)


def map_view(request):
    return render(request, 'map.html')

class PharmacyListAPI(generics.ListAPIView):
    queryset = Pharmacy.objects.filter(owner__is_approved=True)
    serializer_class = PharmacySerializer

# =========================
# SEARCH
# =========================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def search_view(request):
    form = SearchForm(request.GET or None)
    results = PharmacyMedicine.objects.select_related('pharmacy', 'medicine').all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        sort_by = form.cleaned_data.get('sort_by')

        if query:
            results = results.filter(Q(medicine__name__icontains=query))

        lat = request.GET.get('lat')
        lng = request.GET.get('lng')

        if sort_by == 'price':
            results = results.order_by('price')
        elif sort_by == 'distance' and lat and lng:
            try:
                user_lat, user_lng = float(lat), float(lng)
                results = list(results)
                for pm in results:
                    if pm.pharmacy.latitude and pm.pharmacy.longitude:
                        pm.distance = haversine(user_lat, user_lng, pm.pharmacy.latitude, pm.pharmacy.longitude)
                    else:
                        pm.distance = None
                results.sort(key=lambda x: (x.distance is None, x.distance))
            except ValueError:
                pass

    return render(request, 'search.html', {'form': form, 'results': results})


# =========================
# MEDICINE MANAGEMENT
# =========================
@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = PharmacyMedicineForm(request.POST)
        if form.is_valid():
            pharmacy_medicine = form.save(commit=False)
            pharmacy = get_object_or_404(Pharmacy, owner=request.user)
            pharmacy_medicine.pharmacy = pharmacy
            pharmacy_medicine.save()
            messages.success(request, "Medicine added successfully!")
            return redirect('inv')
    else:
        form = PharmacyMedicineForm()
    return render(request, 'add_medicine.html', {'form': form})


@login_required
def inv(request):
    pharmacy = Pharmacy.objects.filter(owner=request.user).first()
    medicines = PharmacyMedicine.objects.filter(pharmacy=pharmacy) if pharmacy else []
    return render(request, 'inv.html', {'medicines': medicines})


@login_required
def edit_medicine(request, pk):
    pharmacy = get_object_or_404(Pharmacy, owner=request.user)
    med = get_object_or_404(PharmacyMedicine, pk=pk, pharmacy=pharmacy)

    if request.method == "POST":
        form = PharmacyMedicineForm(request.POST, instance=med)
        if form.is_valid():
            form.save()
            return redirect("inv")
    else:
        form = PharmacyMedicineForm(instance=med)
    return render(request, "edit_medicine.html", {"form": form})


@login_required
def delete_medicine(request, pk):
    pharmacy = get_object_or_404(Pharmacy, owner=request.user)
    med = get_object_or_404(PharmacyMedicine, pk=pk, pharmacy=pharmacy)

    if request.method == "POST":
        med.delete()
        return redirect("inv")

    return render(request, "delete_medicine.html", {"medicine": med})


# =========================
# STATIC PAGES
# =========================
def home_view(request):
    return render(request, 'home.html')


def about_view(request):
    return render(request, 'about.html', {'year': datetime.now().year})


def contact_view(request):
    return render(request, "contact.html", {"year": datetime.now().year})


