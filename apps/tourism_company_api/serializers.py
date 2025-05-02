from rest_framework import serializers
from apps.tourism_company.models import TourismCompany


class TourismCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourismCompany
        fields = ['company_id',  'company_name', 
                  'company_phone', 'company_address', 'is_active']
