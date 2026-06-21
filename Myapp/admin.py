from django.contrib import admin
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from .models import Viewer
from django.contrib.auth.hashers import make_password
import random

class ViewerBehaviorAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'api_name', 'url', 'timestamp')
    list_filter = ('user', 'action', 'api_name', 'timestamp')
    search_fields = ('user__username', 'action', 'url')
    
    
def generate_random_developer_id():
   
    return random.randint(1000, 9999)
    
def send_developer_credentials(email, name, developerID, password):
    """
    Sends an email with developer credentials to the viewer.
    """
    subject = "Your Developer Credentials"
    message = f"""
    Hello {name},

    Congratulations! You have been promoted to a Developer.

    Your Developer ID is {developerID}.
    Your password is {password}.

    Please log in to the platform using these credentials.

    Best regards,
    Admin Team
    """
    sender_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, sender_email, [email], fail_silently=False)

def approve_form_submissions(modeladmin, request, queryset):
    """
    Approve form submissions by promoting the submitter to a developer.
    """
    for submission in queryset:
        name = submission.name_viewer
        email = submission.email_viewer
        number = submission.number_viewer
        reason = submission.reason

        while True:
            developerID = generate_random_developer_id()
            if not Developer.objects.filter(DeveloperID=developerID).exists():  # Corrected field name
                break 
            
        password = "temporaryPassword" 
        hashed_password = make_password(password)

        viewer, created = Viewer.objects.get_or_create(
            name=name,
            number=number,
            defaults={
                'email_viewer': email,
                'password': hashed_password,
                'role': 'developer', 
            }
        )

        # Create or update Developer entry
        Developer.objects.update_or_create(
            DeveloperID=developerID,  # Corrected field name
            defaults={
                'password': hashed_password,
                'is_active': True,
            }
        )

        # Send developer credentials via email
        send_developer_credentials(email, name, developerID, password)

    modeladmin.message_user(request, "Developer credentials have been sent for approved form submissions.")

approve_form_submissions.short_description = "Approve and promote selected form submitters to developers"



class FormSubmissionAdmin(admin.ModelAdmin):

    list_display = ['name_viewer', 'email_viewer', 'number_viewer', 'reason']
    actions = [approve_form_submissions]  


class ViewerAdmin(admin.ModelAdmin):
    """
    Admin panel for managing viewers.
    """
    list_display = ['name', 'email', 'role']

class DeveloperAdmin(admin.ModelAdmin):
    
    list_display = ['DeveloperID', 'is_active'] 
    search_fields = ['DeveloperID']
    
admin.site.register(Viewer, ViewerAdmin)
admin.site.register(FormSubmission, FormSubmissionAdmin)
admin.site.register(ViewerBehaviour, ViewerBehaviorAdmin)
admin.site.register(Admin)
admin.site.register(Developer,DeveloperAdmin)
