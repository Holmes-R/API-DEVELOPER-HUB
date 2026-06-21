from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.timezone import now,timedelta
import random 
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
def validate_number(value):
    if len(str(value)) != 10: 
        
        raise ValidationError("Phone number must be exactly 10 digits.")

class Viewer(models.Model):
    name = models.CharField(null=False, max_length=50)
    age = models.CharField(null=False, max_length=3)
    address = models.CharField(null=False, max_length=100)
    number = models.BigIntegerField(unique=True,validators=[validate_number])  
    email = models.EmailField(null=False, max_length=100,default=' ') 
    user_otp = models.CharField(max_length=6, blank=True, null=True)
    generated_otp = models.CharField(max_length=6, blank=True, null=True)  
    otp_expiry = models.DateTimeField(blank=True, null=True)
    role = models.CharField(max_length=20,default='Viewer',editable=False)
    def __str__(self):
        return "Viewer: " + self.name

    class Meta:
        verbose_name_plural = "Viewers"
        
    def generate_otp(self):
    
        self.generated_otp = str(random.randint(100000, 999999))
        self.otp_expiry = datetime.now() + timedelta(minutes=5)  
        self.save()
    
    
def validate_developer(value):
    if len(str(value)) != 4:  
        raise ValidationError("Enter correct ID (exactly 4 digits).")
class Developer(models.Model):
    DeveloperID = models.BigIntegerField(
        primary_key=True, 
        validators=[validate_developer]
    )
    password = models.CharField(null=False, max_length=8)
    is_active = models.BooleanField(default=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return self.is_active

    def __str__(self):
        return "Developer: " + str(self.DeveloperID)

    class Meta:
        verbose_name_plural = "Developers"

    
class Admin(models.Model):
    ViewerName = models.ForeignKey(Viewer,blank=False,on_delete=models.CASCADE)
    DeveloperName = models.ForeignKey(Developer,blank=False,on_delete = models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Admin"
  
  
  
class ViewerBehaviour(models.Model):
    user = models.ForeignKey(Viewer,on_delete=models.CASCADE)
    action = models.CharField(max_length = 50)
    api_name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.action} on {self.url} at {self.timestamp}"
    
    class Meta:
        verbose_name_plural = "Viewer Behaviour"


    
class FormSubmission(models.Model):
    name_viewer = models.CharField(null=False, max_length=50)
    email_viewer = models.EmailField(null=False, max_length=100)
    number_viewer = models.BigIntegerField(unique=True)
    reason = models.TextField(max_length=200)
    def __str__(self):
        return f"{self.name_viewer} --> {self.reason}"
    
    class Meta:
        verbose_name_plural = "Viewer -> Admin : Form Submission"
        
       
"""
Use null=True for fields that are not required for all instances of the models.
Use blank=True when you want to allow users to leave certain form fields empty.
"""
    
    
    