from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=256, unique=True)
    assignedTo = models.ForeignKey('auth.User', null=True)

    class Meta:
        ordering = ['name']


class Method(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        ordering = ['name']


class Instance(models.Model):
    text = models.CharField(max_length=1024)
    task = models.ForeignKey('Task')
    info = models.CharField(max_length=1028, blank=True)

    class Meta:
        unique_together = ('text', 'task')


class InstancePool(models.Model):
    name = models.CharField(max_length=256)
    task = models.ForeignKey('Task')
    instances = models.ManyToManyField('Instance')
    selected = models.BooleanField()

    def num_instances(self):
        return self.instances.count()

    def num_unannotated(self):
        return self.instances.filter(annotation__isnull=True).count()

    class Meta:
        unique_together = ('name', 'task')


class Prediction(models.Model):
    method = models.ForeignKey('Method')
    task = models.ForeignKey('Task')
    instance = models.ForeignKey('Instance')
    ranking = models.IntegerField()

    class Meta:
        ordering = ['ranking']


class Annotation(models.Model):
    instance = models.ForeignKey('Instance')
    user = models.ForeignKey('auth.User')
    value = models.CharField(max_length=256)
