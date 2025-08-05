from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    lname = models.CharField(max_length=40,default='')
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name



class PC(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

class Finance(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name


class Technical(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name


class Mechanic(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/MechanicProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    skill = models.CharField(max_length=500,null=True)
    salary=models.PositiveIntegerField(null=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Request(models.Model):
    cat=(('major','major'),('minor','minor'),('routine service','routine service'))
    pcs =(('mmoyo','mmoyo'),('lmaguwu','lmaguwu'),('pmuzavazi','pmuzavazi'),
          ('dgatsi','dgatsi'),('ftasara','ftasara'),('ntsvangirai','ntsvangirai'),
          ('bmudhumo','bmudhumo'),('emukaronda','emukaronda'))
    fins = (('mmware','mmware'),('mmakayi','mmakayi'))
    tec = (('amtambara','amtambara'),)

    lab_man = (('manager1','manager1'),('manager2','manager2'),('manager3','manager3'))


    category=models.CharField(max_length=50,choices=cat)

    #vehicle_no=models.PositiveIntegerField(null=False)
    vehicle_reg = models.CharField(max_length=40,null=False)
    vehicle_model = models.CharField(max_length=40,null=False)
    vehicle_brand = models.CharField(max_length=40,null=False)

    problem_description = models.CharField(max_length=500,null=False)
    date=models.DateField(auto_now=True)
    cost=models.PositiveIntegerField(null=True)
    date1=models.DateField(auto_now=True)

    customer1=models.CharField(max_length=40,default='')

    customer=models.CharField(max_length=40,default='')
    mechanic=models.CharField(max_length=40,default='None')

    stat=(('Pending','Pending'),('Approved','Approved'),('Repairing','Repairing'),('Repairing Done','Repairing Done'),('Released','Released'))
    status=models.CharField(max_length=50,choices=stat,default='Pending',null=True)

    pc_approved = models.CharField(max_length=40,default='No')    
    pc_approved_date = models.CharField(max_length=40,default='.')    
    pc_rejected_date = models.CharField(max_length=40,default='.')    

    pc = models.CharField(max_length=40,choices=pcs)
    reasons = models.CharField(max_length=4000,default='')
    #pc1=models.ForeignKey('Customer', on_delete=models.DO_NOTHING,null=True)


    finance = models.CharField(max_length=40,choices=fins)
    technical = models.CharField(max_length=40,default='amtambara')
    lab_manager = models.CharField(max_length=40,choices=lab_man)


    finance_approved = models.CharField(max_length=40,default='No')
    finance_approved_date = models.CharField(max_length=40,default='.')
    finance_rejected_date = models.CharField(max_length=40,default='.')

    job_open = models.CharField(max_length=40,default='No')
    job_open_date = models.CharField(max_length=40,default='.')

    technical_approved = models.CharField(max_length=40,default='No')
    technical_approved_date = models.CharField(max_length=40,default='.')
    technical_rejected_date = models.CharField(max_length=40,default='.')

    lab_approved = models.CharField(max_length=40,default='No')
    lab_approved_date = models.CharField(max_length=40,default='.')
    lab_rejected_date = models.CharField(max_length=40,default='.')

    technical_fin_approved = models.CharField(max_length=40,default='No')
    technical_fin_approved_date = models.CharField(max_length=40,default='.')
    technical_fin_rejected_date = models.CharField(max_length=40,default='.')

    subs = models.CharField(max_length=40,default='0')
    supplier_justification = models.CharField(max_length=1000,default='0')
    assessement_id = models.CharField(max_length=40,default='0')
    supplier_accepted = models.CharField(max_length=40,default='No')
    supplier_accepted_date = models.CharField(max_length=40,default='.')
    supplier_rejected_date = models.CharField(max_length=40,default='.')

    supplier_done = models.CharField(max_length=40,default='No')
    supplier_done_date = models.CharField(max_length=40,default='.')






    def __str__(self):
        return self.problem_description

class Attendance(models.Model):
    mechanic=models.ForeignKey('Mechanic',on_delete=models.CASCADE,null=True)
    date=models.DateField()
    present_status = models.CharField(max_length=10)

class Feedback(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=40)
    message=models.CharField(max_length=500)


class Assessments(models.Model):
    mechanic=models.CharField(max_length=100,default='1') 
    job=models.CharField(max_length=100,default='1') 
    assessment = models.TextField(max_length=1000) 
    quotation = models.CharField(max_length=500) 
    dos = models.CharField(max_length=500,default='.') 

    def __str__(self):
        return self.mechanic +' '+ self.job
    

class Service(models.Model):
    values = models.CharField(max_length=2000)
    reg_num = models.TextField()
    service = models.TextField()
    mechanic = models.TextField(default="")
    doc = models.TextField(default=".")
    assessment_id = models.TextField(default="")
    request_id = models.TextField(default="")
    manager_approved = models.TextField(default="No")
    manager_approved_date = models.TextField(default=".")
    manager_rejected_date = models.TextField(default=".")

    cos = models.TextField(default="0")
    invoice = models.TextField(default=".")
    next_service = models.TextField(default="0")
    tech = models.TextField(default="amtambara")
    tech_approved = models.TextField(default="No")
    tech_approved_date = models.TextField(default=".")
    tech_rejected_date = models.TextField(default=".")

    POP = models.TextField(default="")
    POP_date = models.TextField(default=".")

    lab_manager = models.TextField(default="manager1")



    def __str__(self):
        return self.mechanic +' '+ self.reg_num
    

class Bike(models.Model):
    reg_num = models.CharField(max_length=20)
    District = models.TextField()
    Province = models.TextField()
    status = models.TextField()
    status_date = models.TextField(default=".")
    next_service = models.TextField()
    last_service = models.TextField()
    last_service_details = models.TextField()
    estimate_milage = models.TextField()
    yr_procured= models.TextField(default=".")
    reasons_for_non_f = models.TextField(default=".")
    days_of_non_f=models.TextField(default=".")
    age=models.TextField(default=".")

