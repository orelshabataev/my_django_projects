from django.urls import path

from blog.views import index, add_post, about, add_article, register, post_detail, UpdatePage, AddPost, DeletePost

urlpatterns = [
    path('', index, name='home'),
    path('posts/', AddPost.as_view(), name='add_post'),
    path('about/', about, name='about'),
    path('add_article/', add_article, name='add_article'),
    path('register/', register, name='register'),
    path('post/<slug:slug_name>/', post_detail, name='post_detail'),
    path('edit/<int:pk>/', UpdatePage.as_view(), name='edit_page'),
    path('delete/<int:pk>/', DeletePost.as_view(), name='delete'),
]
