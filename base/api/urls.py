from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from . views import MyTokenObtainPairView

urlpatterns = [
    path('',views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.signup_view, name='signup'),

    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.ProfileDeleteView.as_view(), name='profile-delete'),
    path('users_edit/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),
    path('user-profile/<int:user_id>/', views.get_user_profile, name='get_user_profile'),
    path('update-profile/<int:user_id>/', views.update_user_profile, name='update_user_profile'),


]
