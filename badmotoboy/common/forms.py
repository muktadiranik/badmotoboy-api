from django import forms
from badmotoboy.common.models import ContactUs


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs

        fields = ('name', 'email', 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'type': 'email', 'required': 'required'})
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'rows': '5', 'required': 'required'})
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'yourmail@mail.com'})
        self.fields['message'].widget.attrs.update({'placeholder': 'Message'})
