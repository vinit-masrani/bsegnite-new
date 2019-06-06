# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    a_id = models.CharField(db_column='A_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    a_pass = models.CharField(db_column='A_PASS', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admin'


class Announcement(models.Model):
    ca_id = models.CharField(db_column='CA_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    ca_data = models.CharField(db_column='CA_DATA', max_length=150)  # Field name made lowercase.
    ct = models.ForeignKey('Category', models.DO_NOTHING, db_column='CT_ID')  # Field name made lowercase.
    su = models.ForeignKey('Subcategory', models.DO_NOTHING, db_column='SU_ID', blank=True, null=True)  # Field name made lowercase.
    c = models.ForeignKey('Company', models.DO_NOTHING, db_column='C_ID')  # Field name made lowercase.
    ca_datetime = models.DateTimeField(db_column='CA_DATETIME')  # Field name made lowercase.
    ca_desc = models.CharField(db_column='CA_DESC', max_length=500)  # Field name made lowercase.
    ca_head = models.CharField(db_column='CA_HEAD', max_length=300)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'announcement'


class Category(models.Model):
    ct_id = models.AutoField(db_column='CT_ID', primary_key=True)  # Field name made lowercase.
    ct_name = models.CharField(db_column='CT_NAME', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'category'


class Company(models.Model):
    c_id = models.BigIntegerField(db_column='C_ID', primary_key=True)  # Field name made lowercase.
    c_acro = models.CharField(db_column='C_ACRO', max_length=50)  # Field name made lowercase.
    c_name = models.CharField(db_column='C_NAME', max_length=100)  # Field name made lowercase.
    c_isin = models.CharField(db_column='C_ISIN', max_length=30)  # Field name made lowercase.
    c_indus = models.CharField(db_column='C_INDUS', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company'


class Custom(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, db_column='U_ID')  # Field name made lowercase.
    c = models.ForeignKey(Company, models.DO_NOTHING, db_column='C_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'custom'


class Subcategory(models.Model):
    su_id = models.AutoField(db_column='SU_ID', primary_key=True)  # Field name made lowercase.
    ct = models.ForeignKey(Category, models.DO_NOTHING, db_column='CT_ID')  # Field name made lowercase.
    su_name = models.CharField(db_column='SU_NAME', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'subcategory'


class Users(models.Model):
    u_id = models.CharField(db_column='U_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    u_name = models.CharField(db_column='U_NAME', max_length=50)  # Field name made lowercase.
    u_pass = models.CharField(db_column='U_PASS', max_length=30)  # Field name made lowercase.
    u_phno = models.BigIntegerField(db_column='U_PHNO')  # Field name made lowercase.
    u_email = models.CharField(db_column='U_EMAIL', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'
