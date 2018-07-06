from django.db import models


# Create your models here.


class College(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=64)
    acronym = models.CharField(max_length=8, unique=True)
    contact = models.EmailField()

    def __str__(self):
        return self.acronym


class Teacher(models.Model):
    name = models.CharField(max_length=128)

    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=128)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField()
    db_folder = models.CharField(max_length=50)
    dropped_out = models.BooleanField(default=False)

    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Mocktest(models.Model):
    problem1 = models.IntegerField()
    problem2 = models.IntegerField()
    problem3 = models.IntegerField()
    problem4 = models.IntegerField()
    totals = models.IntegerField()

    student = models.OneToOneField(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Student {self.student.name} marks"
