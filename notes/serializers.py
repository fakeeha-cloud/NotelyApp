from rest_framework import serializers
from notes.models import User ,Task

class UserSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    password=serializers.CharField(read_only=True)

    class Meta:
        model=User
        fields=['id','username','email','password1','password2','phone','password']

    def create(self, validated_data):                                                           #overrinding create() method
        print('validated data',validated_data)
        #validated data= {'username': 'react', 'email': 'r@gmail.com', 'password1': 'Password@123', 'password2': 'Password@123', 'phone': '111111'}
        
        password1=validated_data.pop('password1')                                       #removing password1 from validated data

        password2=validated_data.pop('password2')

        return User.objects.create_user(**validated_data,password=password1)           #create_user():used to ensure passwords are securely hashed during user creation.,,only one password when doing save so add it


    def validate(self, data):                                                          #overridind valiadate() method for password validation   

        if data['password1']!=data['password2']:
            raise serializers.ValidationError('Password mismatch')
        return data 
    

class TaskSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField(read_only=True)                        #  display owner as string 
    class Meta:
        model=Task
        fields='__all__'
        read_only_fields=['id','created_date','is_active','owner']