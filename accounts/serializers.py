from rest_framework import serializers
from .models import Customer
import datetime

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['pk', 'username', 'email', 'password', 'phone_number', 'profile_photo', 
            'gender', 'date_of_birth'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # check if email user with this email exist then redirect to login
        print(validated_data)
        user = Customer.objects.create(**validated_data)
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()
        return user

    def validate_date_of_birth(self, value):
        """
        It should be in past, before today
        """
        today = datetime.date.today()
        if value > today:
            raise serializers.ValidationError("Birthdate can not be in future.")
        return value
    
    def validate_profile_photo(self, value):
        IMG_FILE_LIMIT = 2048 # in KB
        VALID_EXTENTION = ['png', 'jpeg', 'jpg']

        file_size = value.size / 1000 # convereting bytes to KB
        image_type = value.content_type
        ext = image_type.split('/')[-1]

        if file_size >= IMG_FILE_LIMIT:
            raise serializers.ValidationError("Image file should be less than 2 MB.")
        
        if ext not in VALID_EXTENTION:
            raise serializers.ValidationError(
                "Only image file with extention 'jpg', 'png'and 'jpeg' are allowed."
            ) 
        return value

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    model = Customer
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
