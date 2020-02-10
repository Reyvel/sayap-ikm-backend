from django.shortcuts import render
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from rest_flex_fields import FlexFieldsModelViewSet
from sayap_ikm.core import models, serializers, briapi
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, Exists, OuterRef
from django.db.models.functions import Coalesce

User = get_user_model()

# Create your views here.

class UserFilterSet(filters.FilterSet):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'role')


class UserViewSet(FlexFieldsModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permit_list_expands = ('companies', 'investments', 'holds', 'friends')
    filterset_class = UserFilterSet
    search_fields = ('first_name', 'last_name',)

    @action(detail=False, methods=('GET',))
    def connections(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.queryset.filter(friends=user)
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=('POST',))
    def add(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        user.friends.add(instance)

        return Response()

    @action(detail=True, methods=('POST',))
    def remove(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        user.friends.remove(instance)

        return Response()

    @action(detail=False, methods=('POST',))
    def topup(self, request, *args, **kwargs):
        serializer = serializers.TopupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            amount = serializer.data.get('amount')
            user.top_up = amount
            user.save()
            resp = briapi.create_order(user, amount)

            if resp['status']:
                return Response({
                    'briva_no': '77777',
                    'customer_code': resp['data']['custCode'],
                    'amount': amount
                })
            else:
                return Response(resp, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=('GET',))
    def check_order(self, request, *args, **kwargs):
        customer_code = request.query_params.get('customer_code')
        user = User.objects.get(customer_code=customer_code)
        if user:
            return Response({'amount': user.top_up})
            # customer_code = user.customer_code
            # return Response(briapi.get_order(customer_code))
        return Response(
            {"error": "no customer code found"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=('POST',))
    def finish_order(self, request, *args, **kwargs):
        customer_code = request.data.get('customer_code')
        user = User.objects.get(customer_code=customer_code)
        if user:
            customer_code = user.customer_code
            # resp = briapi.get_order(customer_code) 
            user.balance += user.top_up
            user.save()
            return Response()
        return Response(
            {"error": "no customer code found"},
            status=status.HTTP_400_BAD_REQUEST
        )


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

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated \
            and self.request.user.role == 'OW':
            qs = qs.filter(owners=self.request.user)

        return qs

    def perform_create(self, serializer):
        serializer.save(
            owners=[self.request.user]
        )

    @action(detail=True, methods=('POST',))
    def invest(self, request, *args, **kwargs):
        company = self.get_object()
        instance = models.CompanyInvest.objects.create(
            user=request.user,
            company=company,
            amount=request.data.get('amount')
        )

        user.balance -= amount * company.share_price
        user.save()

        self.serializer_class = serializers.CompanyInvestSerializer
        serializer = self.get_serializer(instance)

        return Response(serializer.data)
        
    @action(detail=False, methods=('GET',))
    def my(self, request, *args, **kwargs):
        invested = models.CompanyInvest.objects.filter(
           user=self.request.user,
           company=OuterRef('pk')
        )
        self.queryset = self.queryset.annotate(
            is_invested=Exists(invested)
        ).filter(
            is_invested=True
        )

        return self.list(request, *args, **kwargs)

class ProjectFilterSet(filters.FilterSet):
    class Meta:
        model = models.Project
        exclude = ('image', 'prospectus',)

class ProjectViewSet(FlexFieldsModelViewSet):
    queryset = models.Project.objects.annotate(
        funded=Coalesce(Sum('investments__amount'), 0)
    )
    serializer_class = serializers.ProjectSerializer
    filterset_class = ProjectFilterSet
    permit_list_expands = ('company', 'reports', 'investments',)

    @action(detail=False, methods=('GET',))
    def my(self, request, *args, **kwargs):
        invested = models.ProjectInvest.objects.filter(
           user=self.request.user,
           project=OuterRef('pk')
        )
        self.queryset = self.queryset.annotate(
            is_invested=Exists(invested)
        ).filter(
            is_invested=True
        )

        return self.list(request, *args, **kwargs)


    @action(detail=True, methods=('POST',))
    def invest(self, request, *args, **kwargs):
        project = self.get_object()
        instance = models.ProjectInvest.objects.create(
            user=request.user,
            project=project,
            amount=request.data.get('amount')
        )
        user.balance -= amount
        user.save()

        project.n_invests += 1
        self.serializer_class = serializers.ProjectInvestSerializer
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class ReportFilterSet(filters.FilterSet):
    class Meta:
        model = models.Report
        exclude = ('file', 'documentation',)


class ReportViewSet(FlexFieldsModelViewSet):
    queryset = models.Report.objects.all()
    serializer_class = serializers.ReportSerializer
    filterset_class = ReportFilterSet
    permit_list_expands = ('project',)


class CompanyInvestViewSet(FlexFieldsModelViewSet):
    queryset = models.CompanyInvest.objects.all()
    serializer_class = serializers.CompanyInvestSerializer
    filterset_fields = '__all__'
    permit_list_expand = ('company', 'user')


class ProjectInvestViewSet(FlexFieldsModelViewSet):
    queryset = models.ProjectInvest.objects.all()
    serializer_class = serializers.ProjectInvestSerializer
    filterset_fields = '__all__'
    permit_list_expand = ('project', 'user')


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
