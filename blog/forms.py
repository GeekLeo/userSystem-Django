from django import forms


class CreateBlogForm(forms.Form):
    name = forms.CharField(label="主题", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    summary = forms.CharField(label="Summary", widget=forms.Textarea)
    content = forms.CharField(label="Content", widget=forms.Textarea)
