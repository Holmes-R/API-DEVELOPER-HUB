from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import DeveloperDashBoard

from .views import DeveloperLogin
urlpatterns = [
    path('otp/<int:number>/', views.generate_otp, name='generate_otp'),
    path('verify/<int:number>/<int:user_otp>/', views.verify_otp, name='verify_otp'),
    path("api/list/", views.api_list, name="api_list"), 
    path("api/data/<str:api_name>/", views.fetch_api_data, name="fetch_api_data"),  
    path('contribute/',views.form_submission,name='form_submission'),
    path('login/',DeveloperLogin.as_view(),name = 'developer-login'),
    path('refresh/',TokenRefreshView.as_view(), name='token-refresh'),
    path('ddash/',DeveloperDashBoard.as_view(),name='developer-dashboard'),
]
