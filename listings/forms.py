from django import forms
from .models import Listing, ListingImage, ContactRequest


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['host', 'created_at', 'updated_at', 'views_count']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Cozy private room in Lekki Phase 1'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe your space, neighborhood, and ideal flatmate...'}),
            'address': forms.TextInput(attrs={'placeholder': 'Street address'}),
            'city': forms.TextInput(attrs={'placeholder': 'e.g. Lagos'}),
            'state': forms.TextInput(attrs={'placeholder': 'e.g. Lagos State'}),
            'available_from': forms.DateInput(attrs={'type': 'date'}),
            'monthly_rent': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'security_deposit': forms.NumberInput(attrs={'placeholder': '0.00'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        current = cleaned_data.get('current_flatmates')
        maximum = cleaned_data.get('max_flatmates')
        if current is not None and maximum is not None:
            if current > maximum:
                raise forms.ValidationError('Current flatmates cannot exceed maximum flatmates.')
        return cleaned_data


class ListingImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ['image', 'caption', 'is_primary']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Introduce yourself and let the host know why you\'re a great flatmate...'
            })
        }


class SearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'City, area, or keyword...'}))
    city = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    room_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + Listing.ROOM_TYPE_CHOICES
    )
    gender_preference = forms.ChoiceField(
        required=False,
        choices=[('', 'Any')] + Listing.GENDER_PREFERENCE_CHOICES
    )
    furnished = forms.ChoiceField(
        required=False,
        choices=[('', 'Any')] + Listing.FURNISHED_CHOICES
    )
    pets_allowed = forms.BooleanField(required=False)
    has_wifi = forms.BooleanField(required=False)
    has_parking = forms.BooleanField(required=False)
