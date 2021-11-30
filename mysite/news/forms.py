from django import forms


class NewsSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=True)
