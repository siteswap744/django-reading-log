from django import forms
from .models import Book, BookStatus, ReadingLog
from django.utils import timezone
from taggit.models import Tag
from .widgets import CustomRadioSelect
from django.db.models import Count


class ReadingLogSearchForm(forms.Form):
    # 年の選択肢を動的に作る
    start_year = 2019  # 家計簿の登録を始めた年
    end_year = timezone.now().year  # 現在の年
    years = [(year, f"{year}年") for year in reversed(range(start_year, end_year + 1))]
    years.insert(0, (0, ""))  # 空白の選択を追加
    YEAR_CHOICES = tuple(years)

    # 月の選択肢を動的に作る
    months = [(month, f"{month}月") for month in range(1, 13)]
    months.insert(0, (0, ""))
    MONTH_CHOICES = tuple(months)

    # 年の選択
    year = forms.ChoiceField(
        label="年での絞り込み",
        required=False,
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={"class": "form"})
    )

    # 月の選択
    month = forms.ChoiceField(
        label="月での絞り込み",
        required=False,
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={"class": "form"})
    )

    # キーワード
    key_word = forms.CharField(
        label="検索キーワード",
        required=False,
        widget=forms.TextInput(attrs={"class": "form",
                                      "autocomplete": "off",
                                      "placeholder": "書籍・著者・摘要",
                                      })
    )

    # 登録件数が多い順に、件数1以上のタグのみ表示
    # TODO: 指定ユーザのみ、かつ指定ユーザが登録しているログのみカウント対象としたい
    tag_queryset = Tag.objects.all()
    tag_queryset = tag_queryset.annotate(log_count=Count("taggit_taggeditem_items")).filter(log_count__gt=0).order_by("-log_count")
    #MAX_TAG_DISPLAY_NUM = 10
    #if tag_queryset.count() > MAX_TAG_DISPLAY_NUM:
    #    tag_queryset = tag_queryset[:MAX_TAG_DISPLAY_NUM]
    # カテゴリー検索
    tag = forms.ModelChoiceField(
        label="タグでの絞り込み",
        required=False,
        queryset=tag_queryset,
        widget=CustomRadioSelect
    )


class BookCreateForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Book
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form"
            field.widget.attrs["placeholder"] = field.label
            field.widget.attrs["autocomplete"] = "off"


class ReadingLogCreateForm(forms.ModelForm):
    class Meta:
        model = ReadingLog
        fields = ["book", "description", "status", "finish_date", "is_public"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form"
            field.widget.attrs["placeholder"] = field.label
            field.widget.attrs["autocomplete"] = "off"
