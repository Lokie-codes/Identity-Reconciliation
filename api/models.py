from django.db import models

# Create your models here.
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    phoneNumber = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    linkedId = models.IntegerField(null=True, blank=True)

    class LinkPrecedence(models.TextChoices):
        PRIMARY = 'primary', 'Primary'
        SECONDARY = 'secondary', 'Secondary'

    linkPrecedence = models.CharField(
        max_length=10,
        choices=LinkPrecedence.choices,
        default=LinkPrecedence.PRIMARY
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Contact(id={self.id}, phoneNumber={self.phoneNumber}, email={self.email} linkedId={self.linkedId}, linkPrecedence={self.linkPrecedence})"