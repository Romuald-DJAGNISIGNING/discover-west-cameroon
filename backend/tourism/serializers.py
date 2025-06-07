from rest_framework import serializers
from .models import Category, Attraction, LocalSite, TourPlan, TourActivity, TourReview, TourCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AttractionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Attraction
        fields = ['id', 'name', 'description', 'location', 'image', 'category', 'category_id']

class LocalSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalSite
        fields = '__all__'

class TourPlanSerializer(serializers.ModelSerializer):
    guide_name = serializers.StringRelatedField(source='guide', read_only=True)
    attractions = AttractionSerializer(many=True, read_only=True)
    attraction_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Attraction.objects.all(), source='attractions', write_only=True
    )

    class Meta:
        model = TourPlan
        fields = ['id', 'title', 'description', 'price', 'duration_days', 'guide', 'guide_name', 'attractions', 'attraction_ids', 'created_at']

    def create(self, validated_data):
        attractions = validated_data.pop('attractions', [])
        tour_plan = TourPlan.objects.create(**validated_data)
        tour_plan.attractions.set(attractions)
        return tour_plan

    def update(self, instance, validated_data):
        attractions = validated_data.pop('attractions', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.duration_days = validated_data.get('duration_days', instance.duration_days)
        instance.guide = validated_data.get('guide', instance.guide)
        instance.save()
        if attractions:
            instance.attractions.set(attractions)
        return instance

class TourActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourActivity
        fields = ['id', 'name', 'tour_plan', 'activity_type', 'description', 'start_time', 'end_time']

class TourReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourReview
        fields = ['id', 'tour_plan', 'user', 'rating', 'comment', 'created_at']

class TourCategorySerializer(serializers.ModelSerializer): 
    class Meta:
        model = TourCategory
        fields = ['id', 'name', 'description', 'slug']
        extra_kwargs = {'slug': {'read_only': True}}

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.slug = instance.name.lower().replace(' ', '-')
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.slug = instance.name.lower().replace(' ', '-')
        instance.save()
        return instance

