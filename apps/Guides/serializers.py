from rest_framework import serializers
from .models import Guide

class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
fields = [
            'guide_id',  # Or 'id' if you prefer that
            'name',
            'email',
            'phone',
            'dob',
            'gender',
            'about_us',
            'languages',  # This will be serialized as a list of language IDs
            'location',
            'experience',
            'expertise',
            'amount',
            'image',
            'created_at',
        ]