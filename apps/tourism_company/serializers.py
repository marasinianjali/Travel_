from rest_framework import serializers
from . models import TourismCompany


class TourismCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourismCompany
        fields = ['company_id',  'company_name', 
                  'company_phone', 'company_address', 'is_active']

