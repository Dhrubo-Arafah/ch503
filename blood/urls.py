from django.urls import path
from blood import views

urlpatterns=[
    path('', views.home, name='index'),
    path('create-post/', views.create_post, name='create_post'),
    path('update-post/<id>', views.update_post, name='update_post'),
    path('delete-post/<id>', views.delete_post, name='delete_post'),
    path('view-post/<id>', views.view_post, name='view_post'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('add-response/<id>', views.add_response, name='add_response'),
    path('remove-response/<id>', views.remove_response, name='remove_response'),
    path('show-response/<id>', views.show_responses, name='show_response'),
    path('approval/<r_id>/<pk>', views.approve, name='approval'),
    path('search-result', views.search, name='search_result'),
    path('contributions/', views.contributions, name='contributions'),
    path('thank-you/<id>', views.cont_detail, name='cont_detail')
]