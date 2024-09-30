
from django.urls import path
from notes import views
from rest_framework.authtoken.views import ObtainAuthToken
urlpatterns=[
    path('register/',views.UserCreationView.as_view()),
    path('tasks/',views.TaskCreateListView.as_view()),
    path('task/<int:pk>/',views.TaskRetriveUpdateDestroyView.as_view()),
    path('task/summary/',views.TaskSummaryApiView.as_view()),
    path('tasks/categories',views.GetCategoriesAPIView.as_view()),
    path('token/',ObtainAuthToken.as_view())


]