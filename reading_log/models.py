from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager


class Book(models.Model):
    title = models.CharField("タイトル", max_length=128)
    author = models.CharField("著者", max_length=128)
    pages = models.IntegerField("ページ数", blank=True)
    price = models.IntegerField("価格", blank=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title


class BookStatus(models.Model):
    status = models.CharField("状態", max_length=32)

    def __str__(self):
        return self.status


class ReadingLog(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name="書籍")
    description = models.TextField("説明", blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="投稿者",
                                   on_delete=models.CASCADE)
    status = models.ForeignKey(BookStatus, on_delete=models.PROTECT, verbose_name="状態")
    finish_date = models.DateField("読了日", blank=True, null=True)
    is_public = models.BooleanField("公開する", default=True)

    def __str__(self):
        return self.book.title

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["book", "created_by"],
                name="book_created_by_unique"
            ),
        ]
