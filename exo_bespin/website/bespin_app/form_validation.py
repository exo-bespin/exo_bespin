"""Create and validate forms for the ``exo_bespin`` web app

Authors
-------

    - Matthew Bourque

Use
---

    This module is intended to be imported and used by ``view.py`` as such:
    ::

        form = LightcurveForm(request.POST)
            if form.is_valid():
                do_something(form)

Dependencies
------------

    - ``django``
"""

import os

from django import forms


class LightcurveForm(forms.Form):
    """Form for user to enter parameters for lightcurve fitting"""

    filename = forms.CharField(
        label='filename',
        required=True,
        widget=forms.Textarea(attrs={
            'rows':1,
            'cols':60,
            'style':'resize:none;',
            'placeholder': 'e.g. /path/to/params.json'}))

    P_p1_prior = forms.ChoiceField(label='P_p1_prior', choices=[('normal', 'normal'), ('fixed', 'fixed')], required=True)
    P_p1_starting_value = forms.FloatField(label='P_p1_starting_value', min_value=0.0, required=False)

    t0_p1_prior = forms.ChoiceField(label='t0_p1_prior', choices=[('normal', 'normal'), ('fixed', 'fixed')], required=True)
    t0_p1_starting_value = forms.FloatField(label='t0_p1_starting_value', min_value=0.0, required=False)
    t0_p1_hyperparameter1 = forms.FloatField(label='t0_p1_hpyerparameter1', min_value=0.0, required=False)
    t0_p1_hyperparameter2 = forms.FloatField(label='t0_p1_hpyerparameter2', min_value=0.0, required=False)

    p_p1_prior = forms.ChoiceField(label='p_p1_prior', choices=[('normal', 'normal'), ('fixed', 'fixed')], required=True)
    p_p1_starting_value = forms.FloatField(label='p_p1_starting_value', min_value=0.0, required=False)
    p_p1_hyperparameter1 = forms.FloatField(label='p_p1_hpyerparameter1', min_value=0.0, required=False)
    p_p1_hyperparameter2 = forms.FloatField(label='p_p1_hpyerparameter2', min_value=0.0, required=False)

    b_p1_prior = forms.ChoiceField(label='b_p1_prior', choices=[('normal', 'normal'), ('fixed', 'fixed')], required=True)
    b_p1_starting_value = forms.FloatField(label='b_p1_starting_value', min_value=0.0, required=False)
    b_p1_hyperparameter1 = forms.FloatField(label='b_p1_hpyerparameter1', min_value=0.0, required=False)
    b_p1_hyperparameter2 = forms.FloatField(label='b_p1_hpyerparameter2', min_value=0.0, required=False)

    q1_inst_prior = forms.ChoiceField(label='q1_inst_prior', choices=[('normal', 'normal'), ('fixed', 'fixed')], required=True)
    q1_inst_starting_value = forms.FloatField(label='q1_inst_starting_value', min_value=0.0, required=False)
    q1_inst_hyperparameter1 = forms.FloatField(label='q1_inst_hpyerparameter1', min_value=0.0, required=False)
    q1_inst_hyperparameter2 = forms.FloatField(label='q1_inst_hpyerparameter2', min_value=0.0, required=False)

    q2_inst_prior = forms.ChoiceField(label='q2_inst_prior', choices=[('normal', 'normal'), ('fixed', 'fixed')], required=True)
    q2_inst_starting_value = forms.FloatField(label='q2_inst_starting_value', min_value=0.0, required=False)
    q2_inst_hyperparameter1 = forms.FloatField(label='q2_inst_hpyerparameter1', min_value=0.0, required=False)
    q2_inst_hyperparameter2 = forms.FloatField(label='q2_inst_hpyerparameter2', min_value=0.0, required=False)

    ecc_p1_prior = forms.ChoiceField(label='ecc_p1_prior', choices=[('normal', 'normal'), ('fixed', 'fixed')], required=True)
    ecc_p1_starting_value = forms.FloatField(label='ecc_p1_starting_value', min_value=0.0, required=False)

    omega_p1_prior = forms.ChoiceField(label='omega_p1_prior', choices=[('normal', 'normal'), ('fixed', 'fixed')], required=True)
    omega_p1_starting_value = forms.FloatField(label='omega_p1_starting_value', min_value=0.0, required=False)

    a_p1_prior = forms.ChoiceField(label='a_p1_prior', choices=[('normal', 'normal'), ('fixed', 'fixed')], required=True)
    a_p1_starting_value = forms.FloatField(label='a_p1_starting_value', min_value=0.0, required=False)
    a_p1_hyperparameter1 = forms.FloatField(label='a_p1_hpyerparameter1', min_value=0.0, required=False)
    a_p1_hyperparameter2 = forms.FloatField(label='a_p1_hpyerparameter2', min_value=0.0, required=False)

    mdilution_inst_prior = forms.ChoiceField(label='mdilution_inst_prior', choices=[('normal', 'normal'), ('fixed', 'fixed')], required=True)
    mdilution_inst_starting_value = forms.FloatField(label='mdilution_inst_starting_value', min_value=0.0, required=False)

    mflux_inst_prior = forms.ChoiceField(label='mflux_inst_prior', choices=[('normal', 'normal'), ('fixed', 'fixed')], required=True)
    mflux_inst_starting_value = forms.FloatField(label='mflux_inst_starting_value', min_value=0.0, required=False)
    mflux_inst_hyperparameter1 = forms.FloatField(label='mflux_inst_hpyerparameter1', min_value=0.0, required=False)
    mflux_inst_hyperparameter2 = forms.FloatField(label='mflux_inst_hpyerparameter2', min_value=0.0, required=False)

    sigma_w_inst_prior = forms.ChoiceField(label='sigma_w_inst_prior', choices=[('normal', 'normal'), ('fixed', 'fixed')], required=True)
    sigma_w_inst_starting_value = forms.FloatField(label='sigma_w_inst_starting_value', min_value=0.0, required=False)
    sigma_w_inst_hyperparameter1 = forms.FloatField(label='sigma_w_inst_hpyerparameter1', min_value=0.0, required=False)
    sigma_w_inst_hyperparameter2 = forms.FloatField(label='sigma_w_inst_hpyerparameter2', min_value=0.0, required=False)

    nwalkers = forms.IntegerField(label='nwalkers', min_value=0, required=True)
    nsteps = forms.IntegerField(label='nsteps', min_value=0, required=True)
    nburnin = forms.IntegerField(label='nburnin', min_value=0, required=True)

    # Prior parameters need their own ID so their corresponding fields can be shown/hidden
    P_p1_prior.widget.attrs = {'id': 'P_p1_prior'}
    t0_p1_prior.widget.attrs = {'id': 't0_p1_prior'}
    p_p1_prior.widget.attrs = {'id': 'p_p1_prior'}
    b_p1_prior.widget.attrs = {'id': 'b_p1_prior'}
    q1_inst_prior.widget.attrs = {'id': 'q1_inst_prior'}
    q2_inst_prior.widget.attrs = {'id': 'q2_inst_prior'}
    ecc_p1_prior.widget.attrs = {'id': 'ecc_p1_prior'}
    omega_p1_prior.widget.attrs = {'id': 'omega_p1_prior'}
    a_p1_prior.widget.attrs = {'id': 'a_p1_prior'}
    mdilution_inst_prior.widget.attrs = {'id': 'mdilution_inst_prior'}
    mflux_inst_prior.widget.attrs = {'id': 'mflux_inst_prior'}
    sigma_w_inst_prior.widget.attrs = {'id': 'sigma_w_inst_prior'}


    def clean_filename(self):
        """Make sure that the filename exists and is accessible"""

        filename = self.cleaned_data['filename']

        # Ensure the filename exists
        if not os.path.exists(filename):
            raise forms.ValidationError("Provided filename does not exist")

        # Ensure the filename is readable
        if not os.access(filename, os.R_OK):
            raise forms.ValidrationError("Provided filename is not readable")

        return filename

    def get_cleaned_data(self):
        """Return the cleaned data"""

        return self.cleaned_data
