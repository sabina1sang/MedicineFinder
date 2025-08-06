from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .models import PharmacyMedicine, Medicine

class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('pharmacy', 'Pharmacy Owner'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Register as")

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)


SORT_CHOICES = (
    ('price', 'Price (Lowest first)'),
    ('distance', 'Distance (Nearest first)'),
)

class SearchForm(forms.Form):
    query = forms.CharField(
        label="Medicine name",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter medicine name'})
    )
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select()
    )

class PharmacyMedicineForm(forms.ModelForm):
    medicine_name = forms.CharField(
        label="Medicine Name",
        required=True,
        widget=forms.TextInput(attrs={
            "class": "w-full p-3 rounded-md border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
        })
    )
    generic_name = forms.CharField(
        label="Generic Name",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full p-3 rounded-md border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
        })
    )

    class Meta:
        model = PharmacyMedicine
        fields = ['medicine_name', 'generic_name', 'price', 'quantity', 'expiry_date']
        widgets = {
            
            'price': forms.NumberInput(attrs={
                "class": "w-full p-3 rounded-md border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            'quantity': forms.NumberInput(attrs={
                "class": "w-full p-3 rounded-md border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            'expiry_date': forms.DateInput(attrs={
                "type": "date",
                "class": "w-full p-3 rounded-md border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
        }

    def save(self, commit=True):
        medicine_name = self.cleaned_data.get('medicine_name')
        generic_name = self.cleaned_data.get('generic_name')

        # Create or get Medicine
        medicine, created = Medicine.objects.get_or_create(
            name=medicine_name,
            defaults={'generic_name': generic_name}
        )

        # Update generic name if already exists
        if not created and generic_name:
            medicine.generic_name = generic_name
            medicine.save()

        # Link medicine to PharmacyMedicine
        instance = super().save(commit=False)
        instance.medicine = medicine

        if commit:
            instance.save()

        return instance
