from django.contrib import admin
from django.urls import path, include
# from knox import views as knox_views
from .views import RegisterAPI, LoginAPI, LogoutAPI, CustomerAPIView # , user_logout

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('registration/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('<int:pk>/', CustomerAPIView.as_view())
]
