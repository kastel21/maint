from django import forms
from django.contrib.auth.models import User
from . import models

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        #fields=['first_name','last_name','username','password']
        fields = '__all__'
        widgets = {
        'password': forms.PasswordInput()
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        #fields=['address','mobile','profile_pic','lname']
        fields = '__all__'





class PCUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class PCForm(forms.ModelForm):
    class Meta:
        model=models.PC
        fields=['address','mobile','profile_pic']



class FinanceUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class FinanceForm(forms.ModelForm):
    class Meta:
        model=models.Finance
        fields=['address','mobile','profile_pic']


class TechnicalUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class TechnicalForm(forms.ModelForm):
    class Meta:
        model=models.Technical
        fields=['address','mobile','profile_pic']



class MechanicUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class MechanicForm(forms.ModelForm):
    class Meta:
        model=models.Mechanic
        fields=['address','mobile','profile_pic','skill']

class MechanicSalaryForm(forms.Form):
    salary=forms.IntegerField()


class RequestForm(forms.ModelForm):
    class Meta:
        model=models.Request
        fields=['category','pc','vehicle_reg','vehicle_model','vehicle_brand','problem_description','lab_manager']
        widgets = {
        'problem_description':forms.Textarea(attrs={'rows': 3, 'cols': 30})
        }

class AdminRequestForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of customer model will be shown there in html
    customer=forms.ModelChoiceField(queryset=models.Customer.objects.all(),empty_label="Customer Name",to_field_name='id')
    mechanic=forms.ModelChoiceField(queryset=models.Mechanic.objects.all(),empty_label="Mechanic Name",to_field_name='id')
    cost=forms.IntegerField()

class AdminApproveRequestForm(forms.Form):
    #mechanic=forms.ModelChoiceField(queryset=models.Mechanic.objects.all(),empty_label="Mechanic Name",to_field_name='id')
    #cost=forms.IntegerField()
    stat=(('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected'))
    status=forms.ChoiceField( choices=stat)
    problem_description=forms.CharField( 
        widget=forms.TextInput(attrs={'rows': 3, 'cols': 30})
    )




class FinanceApproveRequestForm(forms.Form):
    #mechanic=forms.ModelChoiceField(queryset=models.Mechanic.objects.all(),empty_label="Mechanic Name",to_field_name='id')
    #cost=forms.IntegerField()
    stat=(('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected'))
    status=forms.ChoiceField( choices=stat)
    problem_description=forms.CharField( 
        widget=forms.TextInput(attrs={'rows': 3, 'cols': 30})
    )



class UpdateCostForm(forms.Form):
    cost=forms.IntegerField()

class MechanicUpdateStatusForm(forms.Form):
    stat=(('Approved','Approved'),('Repairing','Repairing'),('Repairing Done','Repairing Done'))
    status=forms.ChoiceField( choices=stat)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['by','message']
        widgets = {
        'message':forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }

#for Attendance related form
presence_choices=(('Present','Present'),('Absent','Absent'))
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    date=forms.DateField()

class AskDateForm(forms.Form):
    date=forms.DateField()


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
