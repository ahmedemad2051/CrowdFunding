from django import forms
from projects.models import Project, Image
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'slug', 'desc', 'tags', 'category', 'total', 'start_date', 'end_date']
        labels = {'desc': 'Description'}

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # change a widget attribute:
        self.fields['title'].widget.attrs = {'class': 'form-control valid', 'placeholder': 'Campaign title'}
        self.fields['slug'].widget.attrs = {'class': 'form-control valid', 'placeholder': 'Campaign slug'}
        self.fields['total'].widget.attrs = {'class': 'form-control valid', 'placeholder': 'Total target'}
        self.fields['desc'].widget.attrs = {'class': 'form-control w-100', 'placeholder': 'Campaign details',
                                            'cols': 30, 'rows': 9}

        # self.fields['tags'].widget = forms.ModelMultipleChoiceField(queryset = Tag.objects.all())
        # self.fields['tags'].widget.
        self.fields['tags'].widget.attrs = {'class': 'form-control valid js-tags-multiple'}
        self.fields['category'].widget.attrs = {'class': 'form-control valid'}
        self.fields['start_date'].widget = DateTimePicker()
        self.fields['end_date'].widget = DateTimePicker()
        self.fields['start_date'].widget.attrs = {'class': 'form-control valid', 'placeholder': 'Start date'}
        self.fields['end_date'].widget.attrs = {'class': 'form-control valid', 'placeholder': 'End date'}

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if (start_date and end_date) and (end_date < start_date):
            msg = u"End date should be greater than start date."
            self._errors["end_date"] = self.error_class([msg])


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Images')

    class Meta:
        model = Image
        fields = ('image',)

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs = {'id': 'gallery-photo-add', 'multiple': 'multiple', 'class': 'form-control'}

    # def clean(self):
    #     cleaned_data = super(ImageForm, self).clean()
    #     print(cleaned_data)
    #     image_list = cleaned_data.get("image")
    #     if image_list:
    #         msg = u"End date should be greater than start date."
    #         self._errors["image"] = self.error_class([msg])
