from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class Course(models.Model):
    class CourseType(models.TextChoices):
        ONETOONE = 'OO', _('One to One')
        ONETOMANY = 'OM', _('One to Many')

    kd_mk = models.CharField(max_length=12, primary_key=True)
    nm_mk = models.CharField(max_length=256)
    sks = models.IntegerField()
    course_type = models.CharField(
        max_length=2,
        choices=CourseType.choices,
    )
    is_allowed_new_topic = models.BooleanField()
    topic_count = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'courses'

    def __str__(self):
        return self.nm_mk

class CourseInformation(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    html = RichTextField()

    def __str__(self):
        return self.html
    
class Prerequisite(models.Model):
    class PrerequisiteType(models.TextChoices):
        SKS = 'SKS', _('Jumlah SKS')
        SEMESTER = 'SMT', _('Semester')
        COURSE = 'CRS', _('Mata Kuliah')
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=3,
        choices=PrerequisiteType.choices,
        default=PrerequisiteType.SKS,
    )
    minimum = models.IntegerField(default=0)
    maximum = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.type

class ActivityStep(models.Model):
    class StepType(models.TextChoices):
        INF = 'INF', _('Step Information')
        ASG = 'ASG', _('Step Assignment')
        SID = 'SID', _('Step Sidang')
        
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    index = models.IntegerField()
    name = models.CharField(max_length=256)
    type = models.CharField(
            max_length=3,
            choices=StepType.choices,
            default=StepType.INF,
        )
    
    class Meta:
        unique_together = ('course', 'index')

    def __str__(self):
        return self.name
    
class StepInformation(models.Model):        
    activity_step = models.OneToOneField(ActivityStep, on_delete=models.CASCADE)
    heading = models.CharField(max_length=256, null=True)
    subheading = models.CharField(max_length=256, null=True)
    html = RichTextField()
    
    def __str__(self):
        return self.html
    
class StepSidang(models.Model):
    activity_step = models.OneToOneField(ActivityStep, on_delete=models.CASCADE)
    heading = models.CharField(max_length=256)
    subheading = models.CharField(max_length=256)
    paragraph = models.TextField()
    
    def __str__(self):
        return self.heading
    
class StepAssignment(models.Model):
    activity_step = models.OneToOneField(ActivityStep, on_delete=models.CASCADE)
    heading = models.CharField(max_length=256, null=True)
    subheading = models.CharField(max_length=256, null=True)
    
    def __str__(self):
        return self.heading

class StepComponent(models.Model):
    class AssignmentComponentType(models.TextChoices):
        INF = 'INF', _('Information Component')
        ASG = 'ASG', _('Assignment Component')
        ANN = 'ANN', _('Announcement Component')

    activity_step = models.ForeignKey(ActivityStep, related_name='stepcomponents', on_delete=models.CASCADE)
    index = models.IntegerField()
    type = models.CharField(
            max_length=3,
            choices=AssignmentComponentType.choices,
            default=AssignmentComponentType.INF,
        )
    
    class Meta:
        unique_together = ('activity_step', 'index')

class InformationComponent(models.Model):        
    step_component = models.OneToOneField(StepComponent, related_name='informationcomponents', on_delete=models.CASCADE)
    heading = models.CharField(max_length=256)
    subheading = models.CharField(max_length=256)
    paragraph = models.TextField()
    
    def __str__(self):
        return self.heading
    
class AnnouncementComponent(models.Model):        
    step_component = models.ForeignKey(StepComponent, related_name='announcementcomponents', on_delete=models.CASCADE)
    heading = models.CharField(max_length=256)
    subheading = models.CharField(max_length=256)
    paragraph = models.TextField()
    
    def __str__(self):
        return self.heading
    
class AssignmentComponent(models.Model):
    class AssignmentType(models.TextChoices):
        LOG = 'LOG', _('Log Assignment')
        SUB = 'SUB', _('Submission Assignent')

    step_component = models.OneToOneField(StepComponent, related_name='assignmentcomponents', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    subtitle = models.CharField(max_length=256)
    description = models.TextField()
    type = models.CharField(
            max_length=3,
            choices=AssignmentType.choices,
            default=AssignmentType.SUB,
        )
    
    def __str__(self):
        return self.title