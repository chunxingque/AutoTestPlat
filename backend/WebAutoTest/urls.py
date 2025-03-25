from django.urls import path
from rest_framework import routers

from . import views
router = routers.SimpleRouter()

router.register('project', views.ProjectModelViewSet)

urlpatterns = [
    path('case/',views.WebTestCaseModelViewSet.as_view({"get": "list","post": "create"})),
    path('case/<int:pk>/',views.WebTestCaseModelViewSet.as_view({"get": "retrieve","put": "update","delete": "destroy"})),
    path('casestep/<int:case_id>/',views.WebTestCaseStepInfoAPIView.as_view()),
    path('webstep/',views.WebTestStepGenericViewSet.as_view({"get": "list","post": "create"})),
    path('webstep/<str:pk>/',views.WebTestStepGenericViewSet.as_view({"get": "get_pk","put": "update","delete": "delete"})),
    path('webstepordersort/',views.WebStepOrderSort.as_view()),
    path('runcase/',views.RunCaseTask.as_view()),
    path('projectselect/',views.ProjectSelectGenericAPIView.as_view()),
    path('webcasestepcopy/',views.WebCaseStepCopy.as_view()),
]

urlpatterns += router.urls