from rest_framework import serializers
from apps.tour_package.models import TourPackage, TourismCompany

class TourPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPackage
        fields = [
            'package_id', 'package_name', 'company', 'date',
            'description', 'amount', 'duration', 'country',
            'city', 'tour_type', 'created_at', 'is_approved'
        ]

class TourismCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourismCompany
        fields = ['company_id', 'company_name', 'company_phone', 'company_address', 'is_active']

        read_only_fields = ['company_id', 'is_active']  # Make company_id and is_active read-only
        extra_kwargs = {
            'company_name': {'required': True},
            'company_phone': {'required': True},
            'company_address': {'required': True}
        }