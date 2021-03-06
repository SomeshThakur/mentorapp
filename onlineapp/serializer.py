from rest_framework import serializers

from onlineapp.models import *


class CollegeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=128)
    location = serializers.CharField(max_length=64)
    acronym = serializers.CharField(max_length=8)
    contact = serializers.EmailField()

    def create(self, validated_data):
        """
        Create and return a new `College` instance, given the validated data.
        """
        return College.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `College` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.acronym = validated_data.get('acronym', instance.acronym)
        instance.contact = validated_data.get('style', instance.contact)
        instance.save()
        return instance


class MocktestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mocktest
        fields = ['problem1', 'problem2', 'problem3', 'problem4', 'totals']


class StudentDetailsSerializer(serializers.ModelSerializer):
    mocktest = MocktestSerializer()

    class Meta:
        model = Student
        fields = ('id', 'name', 'dob', 'email', 'db_folder', 'dropped_out', 'mocktest')

    def create(self, validated_data):
        print("c valdiated data: ", validated_data)
        mock_data = dict(validated_data.pop('mocktest'))
        student = Student.objects.create(**validated_data)
        Mocktest.objects.create(student=student, **mock_data)
        return student

    def update(self, instance, validated_data):
        print("u validated data", validated_data)
        instance.name = validated_data.get("name", instance.name)
        instance.dob = validated_data.get("dob", instance.dob)
        instance.email = validated_data.get("email", instance.email)
        instance.db_folder = validated_data.get("db_folder", instance.db_folder)
        instance.dropped_out = validated_data.get("dropped_out", instance.dropped_out)
        instance.college_id = validated_data.get("college_id", instance.college_id)

        mockdata = validated_data["mocktest"]
        print('md ', mockdata)
        if not hasattr(instance, "mocktest"):
            mocktestdata = {'problem1': 0, 'problem2': 0, 'problem3': 0, 'problem4': 0}
            mock = Mocktest.objects.create(Student=instance, **mocktestdata)
            setattr(instance, "mocktest", mock)

        instance.mocktest.problem1 = mockdata.get('problem1', instance.mocktest.problem1)
        instance.mocktest.problem2 = mockdata.get('problem2', instance.mocktest.problem2)
        instance.mocktest.problem3 = mockdata.get('problem3', instance.mocktest.problem3)
        instance.mocktest.problem4 = mockdata.get('problem4', instance.mocktest.problem4)
        instance.mocktest.totals = instance.mocktest.problem1 + instance.mocktest.problem2 + instance.mocktest.problem3 + instance.mocktest.problem4
        instance.mocktest.save()
        instance.save()
        return instance
