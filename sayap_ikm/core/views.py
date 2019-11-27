from django.shortcuts import render
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from rest_flex_fields import FlexFieldsModelViewSet
from sayap_ikm.core import models, serializers

User = get_user_model()

# Create your views here.

class UserFilterSet(filters.FilterSet):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'role')

class UserViewSet(FlexFieldsModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permit_list_expands = ('companies', 'investments', 'holds',)
    filterset_class = UserFilterSet
    search_fields = ('first_name', 'last_name',)

class CompanyFilterSet(filters.FilterSet):
    class Meta:
        model = models.Company
        exclude = ('image', 'prospectus')


class CompanyViewSet(FlexFieldsModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    filterset_class = CompanyFilterSet
    permit_list_expands = ('owners', 'projects', 'investments', 'yields', 'holds')
    search_fields = ('owners__first_name', 'owners__last_name', 'name', 'description', 'address',)

    def perform_create(self, serializer):
        serializer.save(
            owners=[self.request.user]
        )


class ProjectFilterSet(filters.FilterSet):
    class Meta:
        models = models.Project
        exclude = ('image', 'prospectus',)

class ProjectViewSet(FlexFieldsModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    filterset_class = ProjectFilterSet
    permit_list_expands = ('company', 'reports',)


class ReportFilterSet(filters.FilterSet):
    class Meta:
        model = models.Report
        exclude = ('file', 'documentation',)


class ReportViewSet(FlexFieldsModelViewSet):
    queryset = models.Report.objects.all()
    serializer_class = serializers.ReportSerializer
    filterset_class = ReportFilterSet
    permit_list_expands = ('project',)


class InvestViewSet(FlexFieldsModelViewSet):
    queryset = models.Invest.objects.all()
    serializer_class = serializers.InvestSerializer
    filterset_fields = '__all__'
    permit_list_expand = ('company', 'user')


class YieldViewSet(FlexFieldsModelViewSet):
    queryset = models.Yield.objects.all()
    serializer_class = serializers.YieldSerializer
    filterset_fields = '__all__'
    permit_list_expand = ('company', 'user')


class HoldViewSet(FlexFieldsModelViewSet):
    queryset = models.Hold.objects.all()
    serializer_class = serializers.HoldSerializer
    filterset_fields = '__all__'
    permit_list_expand = ('company', 'user')
