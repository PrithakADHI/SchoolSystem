from django import forms
from .models import Semester, AssignmentAnswer, Material, Assignment

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name', 'start_date', 'end_date']

class AssignmentAnswerForm(forms.ModelForm):
    class Meta:
        model = AssignmentAnswer
        fields = ['pdf']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.template_pack = 'bootstrap5'  # or 'bootstrap5'
        self.helper.add_input(Submit('submit', 'Submit'))

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'pdf']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.template_pack = 'bootstrap5'  # or 'bootstrap5'
        self.helper.add_input(Submit('submit', 'Submit'))

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'question', 'deadline']
        widgets = {
            'deadline': forms.TextInput(attrs={'class': 'datepicker'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.template_pack = 'bootstrap5'  # or 'bootstrap5'
        self.helper.add_input(Submit('submit', 'Submit'))

class MarksForm(forms.ModelForm):
    class Meta:
        model = AssignmentAnswer
        fields = ['marks']