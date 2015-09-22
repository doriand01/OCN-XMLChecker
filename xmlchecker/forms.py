from django import forms

class UserInputForm(forms.Form):
	xml_text_area = forms.Textarea()
