from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('contact/', views.contact_page, name='contact'),
    path('uploads/', views.Upload.as_view(), name='upload'),
    path('register/', views.register_page, name='register'),
    path('user/', views.user_page, name='user'),
    path('details/<uuid:pk>/', views.details, name='details'),
    path('<int:ctl_id>/', views.search, name='search'),
    path('<int:ctl_id>/<int:sbl_id>/', views.search, name='search'),
    path('<int:ctl_id>/<int:sbl_id>/<int:up_id>/', views.details, name='details')
]
