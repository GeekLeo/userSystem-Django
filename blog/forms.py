from django import forms


class CreateBlogForm(forms.Form):
    name = forms.CharField(label="主题", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    summary = forms.CharField(label="Summary", widget=forms.Textarea(attrs={'class': 'form-control'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'class': 'form-control'}))


class CommentForm(forms.Form):
    text = forms.CharField(label="评论内容", widget=forms.Textarea(attrs={'class': 'form-control'}))
