from django import forms

class ClassroomUpdateForm(forms.Form):
	studentone = forms.CharField(label="studentone", max_length=20)
	studenttwo = forms.CharField(label="studenttwo", max_length=20)
	classroom = forms.IntegerField(label="classroom")