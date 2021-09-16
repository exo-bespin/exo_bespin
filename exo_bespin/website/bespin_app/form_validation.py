"""
"""

from django import forms

class ExampleForm(forms.Form):
    """
    """

    rp = forms.FloatField(label='rp', min_value=1E-6, max_value=1E6)

    def get_cleaned_data(self):
        """
        """

        return self.cleaned_data