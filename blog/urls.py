from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),

    path('login', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post-create/', views.PostCreate.as_view(), name='post_create'),
    path('post-edit/<slug:slug>/', views.PostEditView.as_view(), name='post_edit'),
    path('post-delete/<slug:slug>/', views.PostDeleteView.as_view(), name='post_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)