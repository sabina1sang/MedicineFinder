from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Pharmacy, Medicine, PharmacyMedicine

# Custom UserAdmin to show role and approval
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_approved', 'is_staff', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'is_approved')}),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)

# Inline admin for PharmacyMedicine inside Pharmacy
class PharmacyMedicineInline(admin.TabularInline):
    model = PharmacyMedicine
    extra = 1  # show 1 extra blank form

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'phone')
    search_fields = ('name', 'owner__username', 'phone')
    inlines = [PharmacyMedicineInline]

admin.site.register(Medicine)

@admin.register(PharmacyMedicine)
class PharmacyMedicineAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'pharmacy', 'price', 'quantity', 'expiry_date', 'updated_at')
    list_filter = ('expiry_date',)
    search_fields = ('medicine__name', 'pharmacy__name')
