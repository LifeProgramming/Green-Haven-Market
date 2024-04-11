from django.urls import path
from. import views

app_name='messaging'
urlpatterns=[
    path('new/<int:item_pk>/',views.newCoversation, name='new'),
    path('', views.inbox, name='inbox'),
    path('<int:pk>', views.detail, name='detail'),
]