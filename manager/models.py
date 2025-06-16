from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class toDoTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField()
    priority = models.CharField(choices=(('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')), default='None', max_length=10)


    def __str__(self):
        return self.title


class onGoingTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    startDate = models.DateTimeField()
    startedDate = models.DateTimeField(auto_now_add = True)
    endDate = models.DateTimeField()
    priority = models.CharField(choices=(('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')), default='None', max_length=10)
    statusOfBeginning = models.CharField(choices=(('DELAY', 'DELAY'),('INTIME', 'INTIME')), max_length=15)

    def __str__(self):
        return f'{self.title} -> {self.statusOfBeginning}'


class Completed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    priority = models.CharField(choices=(('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')), default='None', max_length=10)
    scheduledDate = models.DateTimeField()
    startedDate = models.DateTimeField(auto_now_add = True)
    statusOfBeginning = models.CharField(choices=(('DELAY', 'DELAY'),('INTIME', 'INTIME')), max_length=15)
    deadLine = models.DateTimeField()
    completedDate = models.DateTimeField(auto_now_add=True)
    statusOfCompletion = models.CharField(choices=(('DELAY', 'DELAY'),('INTIME', 'INTIME')), max_length=15)

    def __str__(self):
        return f'{self.title} -> {self.statusOfCompletion}'

# todo = toDoTasks.objects.create(
#     title = 'ML',
#     description = 'Project',
#     startDate = '2025-07-12',
#     endDate = '2025-08-25',
#     priority = 'High'
# )
