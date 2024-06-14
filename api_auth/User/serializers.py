from rest_framework import serializers

from api_auth.User.UserModel import User

class UserSerializer(serializers.ModelSerializer):

 class Meta:
   model = User
   fields = '__all__'
   extra_kwargs = {'password': {'write_only': True}}


 def create(self, validated_data):
     # Create a user object with all validated fields.
     user_obj = User (**validated_data)

     # Encrypt and set the password to this user.
     user_obj.set_password(validated_data['password'])

     # Save the user in the database
     user_obj.save ()
     return user_obj