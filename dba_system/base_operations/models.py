# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models import QuerySet


class Columns(models.Model):
    table_catalog = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    table_schema = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    table_name = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    column_name = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    ordinal_position = models.IntegerField(blank=True, null=True)
    column_default = models.CharField(db_collation='C', blank=True, null=True)
    is_nullable = models.CharField(max_length=3, db_collation='C', blank=True, null=True)
    data_type = models.CharField(db_collation='C', blank=True, null=True)
    character_maximum_length = models.IntegerField(blank=True, null=True)
    character_octet_length = models.IntegerField(blank=True, null=True)
    numeric_precision = models.IntegerField(blank=True, null=True)
    numeric_precision_radix = models.IntegerField(blank=True, null=True)
    numeric_scale = models.IntegerField(blank=True, null=True)
    datetime_precision = models.IntegerField(blank=True, null=True)
    interval_type = models.CharField(db_collation='C', blank=True, null=True)
    interval_precision = models.IntegerField(blank=True, null=True)
    character_set_catalog = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    character_set_schema = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    character_set_name = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    
    collation_catalog = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    collation_schema = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    collation_name = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    domain_catalog = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    domain_schema = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    domain_name = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    udt_catalog = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    udt_schema = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    udt_name = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    scope_catalog = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    scope_schema = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    scope_name = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    maximum_cardinality = models.IntegerField(blank=True, null=True)
    dtd_identifier = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    is_self_referencing = models.CharField(max_length=3, db_collation='C', blank=True, null=True)
    is_identity = models.CharField(max_length=3, db_collation='C', blank=True, null=True)
    identity_generation = models.CharField(db_collation='C', blank=True, null=True)
    identity_start = models.CharField(db_collation='C', blank=True, null=True)
    identity_increment = models.CharField(db_collation='C', blank=True, null=True)
    identity_maximum = models.CharField(db_collation='C', blank=True, null=True)
    identity_minimum = models.CharField(db_collation='C', blank=True, null=True)
    identity_cycle = models.CharField(max_length=3, db_collation='C', blank=True, null=True)
    is_generated = models.CharField(db_collation='C', blank=True, null=True)
    generation_expression = models.CharField(db_collation='C', blank=True, null=True)
    is_updatable = models.CharField(max_length=3, db_collation='C', blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"information_schema"."columns"'

    @staticmethod
    def get_fields(table_name):
        colmumns: QuerySet = Columns.objects
        return (colmumns.values('column_name', 'data_type')
                .filter(table_name=table_name)
                )