# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models, connection
from django.db.models import QuerySet

from base_operations.dtos import ColumnDataDto


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
    def get_columns(table_name: str) -> QuerySet:
        """
        Select data about columns that there are table
        :param table_name:
        :return: QuerySet as dict with keys: {
                    'column_name', 'data_type',
                    'character_maximum_length',
                    'numeric_precision', 'numeric_precision_radix', 'numeric_scale',
                    'is_nullable', 'column_default'
                }
        character_maximum_length - if it`s limit text type than there is not NULL
        numeric_precision_radix - if it`s numeric than there is not NULL
                                  (if it has value not equals 2 than this type has setting to set scale)
        """
        colmumns: QuerySet = Columns.objects
        return (
            colmumns.values(
                'column_name', 'data_type',
                'character_maximum_length',
                'numeric_precision', 'numeric_precision_radix', 'numeric_scale',
                'is_nullable', 'column_default'
            )
            .filter(table_name=table_name)
        )

    @staticmethod
    def get_column_data(table_name: str, column_name) -> ColumnDataDto:
        raw_data = Columns.get_columns(table_name).filter(column_name=column_name).get()
        return ColumnDataDto(
            name=column_name,
            type=raw_data['data_type'],
            limit=raw_data['character_maximum_length'] or raw_data['numeric_precision'],
            num_scale=raw_data['numeric_scale'],
            not_null=(raw_data['is_nullable'] == 'NO'),
            default_value=raw_data['column_default'],
        )

    @staticmethod
    def add_column(table_name: str, column_data: ColumnDataDto):
        query = f'ALTER TABLE "{table_name}" ADD COLUMN IF NOT EXISTS {column_data.name} {column_data.type}'
        if column_data.limit:
            query += f'({column_data.limit}'
            if column_data.num_scale:
                query += f', {column_data.num_scale}'
            query += ')'

        if column_data.not_null:
            query += ' NOT NULL'
        if column_data.default_value:
            query += f' DEFAULT {column_data.default_value}'

        with connection.cursor() as cursor:
            cursor.execute(query)

    @staticmethod
    def is_numeric_type(type_name):
        numeric_types = [
            'smallint', 'integer', 'bigint',
            'decimal', 'numeric', 'real', 'double precision'
        ]
        return type_name in numeric_types

    @staticmethod
    def change_field(table_name: str, column_name: str, column_data: ColumnDataDto):
        query = f'ALTER TABLE "{table_name}" ADD COLUMN IF NOT EXISTS {column_data.name} {column_data.type}'
        if column_data.limit and not Columns.is_numeric_type(column_data.type):
            query += f'({column_data.limit}'
            if column_data.num_scale:
                query += f', {column_data.num_scale}'
            query += ')'

        if column_data.not_null:
            query += ' NOT NULL'
        if column_data.default_value:
            query += f' DEFAULT {column_data.default_value}'

        with connection.cursor() as cursor:
            query = (
                f'ALTER TABLE "{table_name}" DROP COLUMN IF EXISTS {column_name};'
                f'{query}'
            )
            cursor.execute(query)

    @staticmethod
    def delete_column(table_name: str, column_name: str):
        with connection.cursor() as cursor:
            cursor.execute(
                f'ALTER TABLE "{table_name}" '
                f'DROP COLUMN IF EXISTS {column_name} '
            )

    @staticmethod
    def get_column_types():
        with connection.cursor() as cursor:
            query_text = (
                'SELECT '
                ' pg_catalog.format_type(t.oid, NULL) AS "Name" '
                'FROM pg_catalog.pg_type t '
                '     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace '
                'WHERE (t.typrelid = 0 OR (SELECT c.relkind = \'c\' FROM pg_catalog.pg_class c WHERE c.oid = t.typrelid)) '
                '      AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_type el WHERE el.oid = t.typelem AND el.typarray = t.oid) '
                '      AND pg_catalog.pg_type_is_visible(t.oid) '
            )
            cursor.execute(query_text)
            return cursor.fetchall()

    @staticmethod
    def get_indexes(table_name: str):
        query = (
            'SELECT  indname.relname as index_name, a.attname, i.indisprimary, i.indisunique '
            '   FROM   pg_index i '
            '   JOIN   pg_attribute a ON a.attrelid = i.indrelid '
            '                           AND a.attnum = ANY(i.indkey) '
            '   JOIN   pg_class indname ON indname.oid = i.indexrelid '
           f'WHERE  i.indrelid = \'"public"."{table_name}"\'::regclass '
            'ORDER BY index_name '
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    @staticmethod
    def get_foreign_keys(table_name: str):
        query = (
            'SELECT '
            '   tc.constraint_name, '
            '   kcu.column_name, '
            '   ccu.column_name AS foreign_column_name '
            'FROM information_schema.table_constraints AS tc '
            '   JOIN information_schema.key_column_usage AS kcu '
            '       ON tc.constraint_name = kcu.constraint_name '
            '           AND tc.table_schema = kcu.table_schema '
            '   JOIN information_schema.constraint_column_usage AS ccu '
            '   ON ccu.constraint_name = tc.constraint_name '
            'WHERE tc.constraint_type = \'FOREIGN KEY\' '
            '       AND tc.table_schema=\'public\' '
            f'       AND tc.table_name=\'{table_name}\'; '
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    @staticmethod
    def add_pk(table_name: str, pk_name: str, column_names: list[str]):
        query = (
            f'ALTER TABLE {table_name} '
            f'      ADD CONSTRAINT {pk_name} '
            f'          PRIMARY KEY ({",".join(column_names)});'
        )
        with connection.cursor() as cursor:
            cursor.execute(query)

    @staticmethod
    def delete_pk(table_name: str, pk_name: str):
        query = (
                f'ALTER TABLE {table_name} '
                f'      DROP CONSTRAINT {pk_name}'
        )
        with connection.cursor() as cursor:
            cursor.execute(query)

    @staticmethod
    def add_index(table_name: str, index_name: str, is_unique: bool, column_names: list[str]):
        query = (
            f'CREATE {"UNIQUE" if is_unique else ""} INDEX "{index_name}" '
            f'  ON {table_name} '
            f'  ({",".join(column_names)}) '
        )
        with connection.cursor() as cursor:
            cursor.execute(query)

    @staticmethod
    def delete_index(index_name: str):
        query = (
            f'DROP INDEX IF EXISTS {index_name}'
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
