from rest_framework import routers
from sayap_ikm.core import views

router = routers.DefaultRouter()

router.register('users', views.UserViewSet)
router.register('companies', views.CompanyViewSet)
router.register('projects', views.ProjectViewSet)
router.register('reports', views.ReportViewSet)
router.register('invests', views.InvestViewSet)
router.register('yields', views.YieldViewSet)
router.register('holds', views.HoldViewSet)