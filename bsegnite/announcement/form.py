from django import forms
from .models import Range,Company
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DatePickerInput
from dal import autocomplete


class LoginForm(forms.ModelForm):
	email = forms.EmailField(max_length = 254, required = True)
	password = forms.CharField(widget = forms.PasswordInput(), required = True)
	class Meta:
		model = User
		fields = ('email','password')

class SignupForm(UserCreationForm):
	email = forms.EmailField(max_length=254, required=True)
	password1=forms.CharField(widget=forms.PasswordInput(),required=True)
	password2=forms.CharField(widget=forms.PasswordInput(),required=True)
	
	class Meta:
		model = User
		fields = ('email', 'password1', 'password2')
		

# ListOfCategory = (
#                 (1 , 'AGM/EGM'), 
#                 (2 , 'BOARD MEETING'), 
#                 (3 , 'COMPANY UPDATE'), 
#                 (4 , 'CORP.ACTION'), 
#                 (5 , 'INSIDER TRADING/SAST'), 
#                 (6 , 'NEW LISTING'), 
#                 (7 , 'RESULT'),
#             )


class DateChoose(forms.ModelForm):
	start_date = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'), required = False)
	end_date = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'), required = False)
	# categories = forms.MultipleChoiceField(
	# 	required=False,
	# 	widget = forms.CheckboxSelectMultiple(attrs={'class': 'btn-group spacing alert alert-success'}),
	# 	choices = ListOfCategory
	# 	)
	class Meta:
		model = Range
		fields=('start_date','end_date')

# class CompanyForm(forms.ModelForm):
# 	# Companyc = forms.ModelChoiceField(queryset=Company.objects.all(),widget=autocomplete.ModelSelect2(url='company-autocomplete'))
# 	class Meta:
# 		model = Company
# 		fields = ('__all__')
