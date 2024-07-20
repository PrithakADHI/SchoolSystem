from django.db import models

from django.contrib.auth.models import User

from autoslug import AutoSlugField
from django.utils import timezone
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator

# Create your models here.

class Roles(models.Model):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'

    ROLE_CHOICES = [
        (ADMIN, 'admin'),
        (TEACHER, 'teacher'),
        (STUDENT, 'student')
    ]

class Semester(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    slug = AutoSlugField(populate_from='name', unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Roles.ROLE_CHOICES, default=Roles.STUDENT)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    slug = AutoSlugField(populate_from='name', unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def total_assignments(self):
        return Assignment.objects.filter(chapter__subject=self).count()

class Sgpa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True, related_name='sgpa')
    gpa = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(4.0)])

    def __str__(self):
        return f"{self.user.username} - {self.semester.name} - {self.gpa}"

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="chapters", null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = AutoSlugField(populate_from='name', unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.subject} - {self.name}"
    
    def total_assignments(self):
        return Assignment.objects.filter(chapter=self).count()

class Material(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='materials', null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    pdf = models.FileField(upload_to='materials/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __str__(self):
        return f"{self.chapter.name} - {self.title}"

class Syllabus(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name='syllabus', null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Syllabus of: {self.subject.name}"
    
class Assignment(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='assignment', null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    question = models.TextField(null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True, blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.chapter} - {self.title}"
    
    def unsubmitted_assignments(user):
        submitted_assignments = AssignmentAnswer.objects.filter(user=user).values_list('assignment_id', flat=True)
        return Assignment.objects.exclude(id__in=submitted_assignments).count()

class AssignmentAnswer(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    marks = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    pdf = models.FileField(upload_to="assignments/", null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])