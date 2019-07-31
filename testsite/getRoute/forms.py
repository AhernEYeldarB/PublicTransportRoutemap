from django import forms
from multigtfs.models import Shape

class PostForm(forms.ModelForm):
    class Meta:
        model = Shape
        fields = ['shape_id']
        widgets = {
            'coords':
            forms.TextInput(
                attrs={
                    'id': 'post-text',
                    'required': True,
                    'placeholder': 'Say something...'
                }),
        }