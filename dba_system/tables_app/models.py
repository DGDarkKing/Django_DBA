# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models, connection
from django.db.models import QuerySet


class Tables(models.Model):
    table_catalog = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    table_schema = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    table_name = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    table_type = models.CharField(db_collation='C', blank=True, null=True)
    self_referencing_column_name = models.TextField(db_collation='C', blank=True,
                                                    null=True)  # This field type is a guess.
    reference_generation = models.CharField(db_collation='C', blank=True, null=True)
    user_defined_type_catalog = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    user_defined_type_schema = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    user_defined_type_name = models.TextField(db_collation='C', blank=True, null=True)  # This field type is a guess.
    is_insertable_into = models.CharField(max_length=3, db_collation='C', blank=True, null=True)
    is_typed = models.CharField(max_length=3, db_collation='C', blank=True, null=True)
    commit_action = models.CharField(db_collation='C', blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"information_schema"."tables"'
    #
    #
    #
    # LOGIC
    #
    #
    #
    @staticmethod
    def get_table_names():
        tables: QuerySet = Tables.objects
        return tables.filter(table_schema='public').values('table_name')

    @staticmethod
    def delete_table(table_name):
        cursor = connection.cursor()
        cursor.execute(
            f'DROP TABLE IF EXISTS '
            f'"{table_name}"'
        )

    @staticmethod
    def create_table(table_name):
        cursor = connection.cursor()
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS '
            f'"{table_name}" ()'
        )
