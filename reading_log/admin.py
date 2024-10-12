from django.contrib import admin
from .models import Book, BookStatus, ReadingLog
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class BookResource(resources.ModelResource):
    class Meta:
        model = Book


@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    ordering = ("id",)
    resource_class = BookResource


class BookStatusResource(resources.ModelResource):
    class Meta:
        model = BookStatus


@admin.register(BookStatus)
class BookStatusAdmin(ImportExportModelAdmin):
    ordering = ("id",)
    resource_class = BookStatusResource


class ReadingLogResource(resources.ModelResource):
    class Meta:
        model = ReadingLog


@admin.register(ReadingLog)
class ReadingLogAdmin(ImportExportModelAdmin):
    search_fields = ("description",)
    list_display = ["book", "created_by", "status"]
    list_filter = ("created_by",)
    ordering = ("id",)
    resource_class = ReadingLogResource
