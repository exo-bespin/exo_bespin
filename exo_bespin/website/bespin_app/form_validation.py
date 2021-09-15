"""
"""

from django import forms

class ExampleForm(forms.Form):
    """
    """

    username = forms.CharField(label='Username', max_length=100)

    def clean_username(self):
        """
        """

        username = self.cleaned_data['username']
        return username