from django.db import models

# Create your models here.


class Server(models.Model):
    name_guild = models.CharField(max_length=255)
    desc_guild = models.TextField()
    icon_guild = models.CharField(max_length=255)
    region_guild = models.CharField(max_length=255)
    owner_guild = models.CharField(max_length=255)
    membercount_guild = models.IntegerField()
    createdat_guild = models.DateField()

class Channel(models.Model):
    id_channel = models.BigAutoField(primary_key=True)
    name_channel = models.CharField(max_length=255)
    type_channel = models.CharField(max_length=255)
    createdat_channel= models.DateField()
    position_channel = models.IntegerField()
    id_guild = models.ForeignKey(Server, on_delete=models.CASCADE)

class Member(models.Model):
    id_member = models.BigAutoField(primary_key=True)
    name_member = models.CharField(max_length=255)
    nick_member = models.CharField(max_length=255)
    avatar_member = models.CharField(max_length=255)
    banner_member =  models.CharField(max_length=255)
    joinedat_member= models.DateField()
    status = models.CharField(max_length=20, default="Offline")
    id_guild = models.ForeignKey(Server, on_delete=models.CASCADE)
    
    

class Roles(models.Model):
    id_role = models.BigAutoField(primary_key=True)
    name_role = models.CharField(max_length=255)
    position_role = models.IntegerField()
    members = models.ManyToManyField(Member, through="MemberRole")

    def __str__(self):
        return '%s' % (self.name_role)

class MemberRole(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    date_joined = models.DateField()

class Message(models.Model):
    id_message = models.BigAutoField(primary_key=True)
    content_message = models.TextField() 
    date_message = models.DateField()
    id_member = models.ForeignKey(Member, on_delete=models.CASCADE)
    id_channel = models.ForeignKey(Channel, on_delete=models.CASCADE)


class Event(models.Model):
    id_event = models.AutoField(primary_key=True)
    name_event = models.CharField(max_length=255, null=True, blank=True)
    start_event = models.DateTimeField(null=True,blank=True)
    end_event = models.DateTimeField(null=True,blank=True)
    members_event = models.ManyToManyField(Member, through="MemberEvent")


class MemberEvent(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_joined = models.DateField()