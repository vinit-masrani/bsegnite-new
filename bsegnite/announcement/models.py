from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField


# Create your models here.
class Category(models.Model):
    ct_id = models.AutoField(db_column='ct_id', primary_key=True)  # Field name made lowercase.
    ct_name = models.CharField(db_column='ct_name', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'category'

    def __str__(self):
    	return self.ct_name

    	
class Company(models.Model):
    c_id = models.BigIntegerField(db_column='c_id', primary_key=True)  # Field name made lowercase.
    c_acro = models.CharField(db_column='c_acro', max_length=50)  # Field name made lowercase.
    c_name = models.CharField(db_column='c_name', max_length=100)  # Field name made lowercase.
    c_isin = models.CharField(db_column='c_isin', max_length=30)  # Field name made lowercase.
    c_indus = models.CharField(db_column='c_indus', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company'

    def __str__(self):
    	return self.c_name

    def get_absolute_url(self):
        return "company/%s/" %(self.c_id)


class Subcategory(models.Model):
    su_id = models.AutoField(db_column='su_id', primary_key=True)  # Field name made lowercase.
    ct = models.ForeignKey(Category, models.DO_NOTHING, db_column='ct_id')  # Field name made lowercase.
    su_name = models.CharField(db_column='su_name', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'subcategory'

    def __str__(self):
        return self.su_name



class Announcement(models.Model):
    ca_id = models.CharField(db_column='ca_id', primary_key=True, max_length=100)  # Field name made lowercase.
    ca_data = models.CharField(db_column='ca_data', max_length=150,blank=True)  # Field name made lowercase.
    ct = models.ForeignKey(Category, models.DO_NOTHING, db_column='ct_id')  # Field name made lowercase.
    su = models.ForeignKey(Subcategory, models.DO_NOTHING, db_column='su_id', blank=True, null=True)  # Field name made lowercase.
    c = models.ForeignKey(Company, models.DO_NOTHING, db_column='c_id')  # Field name made lowercase.
    ca_datetime = models.DateTimeField(db_column='ca_datetime')  # Field name made lowercase.
    ca_desc = models.CharField(db_column='ca_desc', max_length=500)  # Field name made lowercase.
    ca_head = models.CharField(db_column='ca_head', max_length=300)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'announcement'
        ordering=('-ca_datetime',)

    def __str__(self):
    	return str(self.ca_head)

    def get_absolute_url(self):
        return "company/%s/" %(self.c_id)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()
# ListOfCategory = (
#                 (1 , 'AGM/EGM'), 
#                 (2 , 'BOARD MEETING'), 
#                 (3 , 'COMPANY UPDATE'), 
#                 (4 , 'CORP.ACTION'), 
#                 (5 , 'INSIDER TRADING/SAST'), 
#                 (6 , 'NEW LISTING'), 
#                 (7 , 'RESULT'),
#             )

class Range(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    # categories = MultiSelectField(choices = ListOfCategory)

    # def company_details(self):
    # 	# return " ".join(map(lambda c:c.c_id,self.c.c_name.all()))
    # 	try:
    # 		return ",".join(map(lambda c:c.c_id,self.c.c_name))
    # 	except:
    # 		return "Error"

class Custom(models.Model):
    u = models.ForeignKey(User, models.DO_NOTHING, db_column='u_id', primary_key=True)  # Field name made lowercase.
    c = models.ForeignKey(Company, models.DO_NOTHING, db_column='c_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'custom'
        unique_together = (('u', 'c'),)

class Customsubcat(models.Model):
    u = models.ForeignKey(User, models.DO_NOTHING, db_column='u_id',primary_key=True)
    su = models.ForeignKey(Subcategory, models.DO_NOTHING, db_column='su_id')

    class Meta:
        managed = False
        db_table = 'customsubcat'
        unique_together = (('u','su'))

class Customcat(models.Model):
    u = models.ForeignKey(User, models.DO_NOTHING, db_column='u_id',primary_key=True)
    su = models.ForeignKey(Subcategory, models.DO_NOTHING, db_column='su_id')

    class Meta:
        managed = False
        db_table = 'customcat'
        unique_together = (('u','su'))
