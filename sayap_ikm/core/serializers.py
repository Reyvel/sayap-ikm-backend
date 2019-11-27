from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from django.contrib.auth import get_user_model
from sayap_ikm.core import models

User = get_user_model()

class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'role', 'image')
        expandable_fields = {
            'companies': (
                'sayap_ikm.core.serializers.CompanySerializer',
                {'source': 'companies', 'many': True}
            ),
            'investments': (
                'sayap_ikm.core.serializers.InvestSerializer',
                {'source': 'investments', 'many': True}
            ),
            'holds': (
                'sayap_ikm.core.serializers.HoldSerializer',
                {'source': 'holds', 'many': True}
            )
        }


class CompanySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Company
        fields = '__all__'
        expandable_fields = {
            'owners': (
                'sayap_ikm.core.serializers.UserSerializer',
                {'source': 'owners', 'many': True}
            ),
            'projects': (
                'sayap_ikm.core.serializers.ProjectSerializer',
                {'source': 'projects', 'many': True}
            ),
            'investments': (
                'sayap_ikm.core.serializers.InvestSerializer',
                {'source': 'investments', 'many': True}
            ),
            'yields': (
                'sayap_ikm.core.serializers.YieldSerializer',
                {'source': 'yields', 'many': True}
            ),
            'holds': (
                'sayap_ikm.core.serializers.HoldSerializer',
                {'source': 'holds', 'many': True}
            )
        }

class ProjectSerializer(FlexFieldsModelSerializer):
    funded = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.Project
        fields = '__all__'
        expandable_fields = {
            'company': (
                'sayap_ikm.core.serializers.CompanySerializer',
                {'source': 'company'}
            ),
            'reports': (
                'sayap_ikm.core.serializers.ReportSerializer',
                {'source': 'reports'}
            )
        }

class ReportSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Report
        fields = '__all__'
        expandable_fields = {
            'project': (
                'sayap_ikm.core.serializers.ProjectSerializer',
                {'source': 'project'}
            )
        }

class CompanyInvestSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.CompanyInvest
        fields = '__all__'
        expandable_fields = {
            'user': (
                'sayap_ikm.core.serializers.UserSerializer',
                {'source': 'user'},
            ),
            'company': (
                'sayap_ikm.core.serializers.CompanySerializer',
                {'source': 'company'}
            )
        }


class ProjectInvestSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectInvest
        fields = '__all__'
        expandable_fields = {
            'user': (
                'sayap_ikm.core.serializers.UserSerializer',
                {'source': 'user'},
            ),
            'project': (
                'sayap_ikm.core.serializers.ProjectSerializer',
                {'source': 'company'}
            )
        }


class YieldSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Yield
        fields = '__all__'
        expandable_fields = {
            'user': (
                'sayap_ikm.core.serializers.UserSerializer',
                {'source': 'user'},
            ),
            'company': (
                'sayap_ikm.core.serializers.CompanySerializer',
                {'source': 'company'}
            )
        }


class HoldSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Hold
        fields = '__all__'
        expandable_fields = {
            'user': (
                'sayap_ikm.core.serializers.UserSerializer',
                {'source': 'user'},
            ),
            'company': (
                'sayap_ikm.core.serializers.CompanySerializer',
                {'source': 'company'}
            )
        }