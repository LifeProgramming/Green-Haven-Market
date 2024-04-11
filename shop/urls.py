from django.urls import path
from . import views

urlpatterns = [
   path('items/',views.itemsList.as_view(), name='items' ),
   path('item/<int:pk>',views.itemDetail.as_view(), name='item-detail' ),
   path('login/', views.LoginUserView.as_view(),name='login'),
   path('logout/', views.logoutUser, name='logout'),
   path('register/', views.RegisterUserView.as_view(), name='register'),
   path('your-addded-items/',views.addedItems.as_view(),name='added-items'),
   path('add-item/', views.itemForm.as_view(),name='add-item'),
   path('edit-item/<int:pk>/', views.updateItem,name='edit-item'),
   path('delete-item/<int:pk>/', views.deleteItem, name='delete-item'),
]