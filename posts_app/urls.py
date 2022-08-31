from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostIndex.as_view(), name='index'),
    path('category/<str:category>',
         views.PostCategory.as_view(), name='category_post'),
    path('search/', views.PostSearch.as_view(), name='search_post'),
    path('post/<int:pk>', views.PostDetails.as_view(), name='detail_post'),
]
