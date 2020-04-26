from django import forms


class SetIplSeasonForm(forms.Form):
    """
    form for creating password
    """

    season = forms.ChoiceField()
