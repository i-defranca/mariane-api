# from rest_framework import serializers
# from .services import create_entry


# class EntryPostSerializer(serializers.Serializer):
#     class Meta:
#         model = Entry
#         fields = '__all__'
#         read_only_fields = ['user', 'created_at']

# metric = serializers.CharField()
# option = serializers.CharField()
# user = self.context['request'].user

# def validate(self, data):
#     entry_type = data["entry_type"]

#     if not entry_type.allow_multiple_per_day:
#         exists = Entry.objects.filter(
#             user=self.context["request"].user,
#             entry_date=data["entry_date"],
#             entry_type=entry_type
#         ).exists()

#         if exists:
#             raise serializers.ValidationError(
#                 "This type already exists for this date."
#             )

#     return data

# def create(self, validated_data):
#     return create_entry(**validated_data)


# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated


# class EntryViewSet(ModelViewSet):
#     serializer_class = EntrySerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Entry.objects.filter(user=self.request.user)
