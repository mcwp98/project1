from django import forms

from models import Photo

class PhotoUpload(forms.ModelForm):
    
    class Meta:
        model = Photo
        fields = ('title', 'original')
