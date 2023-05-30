from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['accept'] = 'video/*' 

    class Meta:
        model = Video
        fields = ('file', 'image')
    