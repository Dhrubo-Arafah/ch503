from django.urls import path

from community import views

urlpatterns = [
    path('', views.community, name='community'),
    path('create/', views.create_group, name='create_group'),
    path('make-request/<id>', views.make_request, name='make_request'),
    path('update_community/<id>', views.update_community, name="update_community"),
    path('my-community/', views.my_community, name="my_community"),
    path('community/<id>', views.single_community, name="community")
]
