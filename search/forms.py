from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput)


class AdvancedSearchForm(forms.Form):
    all_these_words = forms.CharField(required=False, widget=forms.TextInput(attrs={'onkeyup' : 'show_query()'}))
    this_exact_word_or_phrase = forms.CharField(required=False, widget=forms.TextInput(attrs={'onkeyup' : 'show_query()'}))
    any_of_these_words = forms.CharField(required=False, widget=forms.TextInput(attrs={'onkeyup' : 'show_query()'}))
    none_of_these_words = forms.CharField(required=False, widget=forms.TextInput(attrs={'onkeyup' : 'show_query()'}))

