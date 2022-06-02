from tkinter import Widget
from django import forms
from .models import UserPost


class UserPostForm(forms.ModelForm):

    class Meta:
        model = UserPost
        exclude = ('lastupdate', 'created_at', 'author')

    def __init__(self, *args, **kwargs):

        super(UserPostForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = ""
        self.fields['title'].widget = forms.TextInput(
            attrs={
                'autocomplete': "off",
                'value': "",
                'class': "form-control mb-3 mt-3",
                'type': "text",
                'name': "posttitle",
                'id': "posttitle",
                'width': "456px",
                'placeholder': "Post anything...."
            })
        # self.fields['tags'].label = ""

        # self.fields['tags'].widget = forms.TextInput(
        #     attrs={
        #         'class': "form-control mb-3 hideres",
        #         'type': "text",
        #         'name': "tags",
        #         'id': "tags",
        #         "data-role":"tagsinput",
        #         'placeholder': "tags..",
        #     })

        self.fields['body'].label = ""
        self.fields['body'].widget = forms.Textarea(
            attrs={
                'id': "postbody",
                'name': "postbody",
                'class': "form-control mb-3 hideres",
                'rows': "4",
                'placeholder': "body..."
            })
        self.fields['cover_img'].label = ""
        self.fields['cover_img'].widget = forms.ClearableFileInput(
            attrs={
                'type': "file",
                'name': "cover_img",
                'accept': "image/*",
                'class': "clearablefileinput form-control mb-3 form-control-file",
                'id': "id_cover_img"
            })
