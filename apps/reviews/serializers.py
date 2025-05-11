from rest_framework import serializers
from apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'review_id',
            'user',
            'package',
            'guide',
            'hotel',
            'company',
            'rating',
            'review_text',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.review_text = validated_data.get('review_text', instance.review_text)
        instance.save()
        return instance