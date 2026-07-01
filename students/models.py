from django.db import models

class students(models.Model):
    name = models.CharField(max_length=100)
    roll = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(students, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"