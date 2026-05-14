from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Project, Resource, Tag, ResourceTag


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'description']


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        fields = [
            'title',
            'resource_type',
            'file',
            'external_url',
            'authors',
            'publication_year',
            'abstract_text'
        ]

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file:
            allowed_extensions = ['pdf', 'doc', 'docx', 'txt']
            extension = file.name.split('.')[-1].lower()

            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    "Only PDF, DOC, DOCX, and TXT files are allowed."
                )

            max_size = 10 * 1024 * 1024

            if file.size > max_size:
                raise forms.ValidationError(
                    "File size must be under 10MB."
                )

        return file


class ComparisonForm(forms.Form):
    resource_one = forms.ModelChoiceField(
        queryset=Resource.objects.none(),
        label="First Resource"
    )

    resource_two = forms.ModelChoiceField(
        queryset=Resource.objects.none(),
        label="Second Resource"
    )

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

        if project:
            self.fields['resource_one'].queryset = Resource.objects.filter(
                project=project
            )
            self.fields['resource_two'].queryset = Resource.objects.filter(
                project=project
            )

    def clean(self):
        cleaned_data = super().clean()
        resource_one = cleaned_data.get('resource_one')
        resource_two = cleaned_data.get('resource_two')

        if resource_one and resource_two and resource_one == resource_two:
            raise forms.ValidationError(
                "Please select two different resources for comparison."
            )

        return cleaned_data


class TagForm(forms.Form):
    resource = forms.ModelChoiceField(
        queryset=Resource.objects.none(),
        label="Select Resource"
    )

    tag_name = forms.CharField(
        max_length=50,
        label="Tag Name",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. AI, cybersecurity, healthcare'
        })
    )

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

        if project:
            self.fields['resource'].queryset = Resource.objects.filter(
                project=project
            )

    def clean_tag_name(self):
        tag_name = self.cleaned_data.get('tag_name')

        if tag_name:
            tag_name = tag_name.strip().lower()

        return tag_name