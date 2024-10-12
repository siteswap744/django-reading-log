from django.views import generic
from .models import Book, ReadingLog
from .forms import ReadingLogSearchForm, ReadingLogCreateForm, BookCreateForm
from django.db.models import Q
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Page
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import Http404
import numpy as np
import pandas as pd
from django_pandas.io import read_frame
from .plugin_plotly import GraphGenerator
from django.db.models import Sum


class UserGuide(generic.TemplateView):
    template_name = "reading_log/user_guide.html"

    def get_success_url(self):
        return reverse_lazy("reading_log:individual_log", args=[self.request.user.id])

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)


class BookCreate(LoginRequiredMixin, generic.CreateView):
    template_name = "reading_log/register.html"
    model = Book
    form_class = BookCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "書籍登録"
        return context

    def get_success_url(self):
        #return reverse_lazy("reading_log:reading_log_list")
        return reverse_lazy("reading_log:individual_log", args=[self.request.user.id])


class ReadingLogCreate(LoginRequiredMixin, generic.CreateView):
    template_name = "reading_log/register.html"
    model = ReadingLog
    form_class = ReadingLogCreateForm

    # ログインユーザの情報を設定する
    def form_valid(self, form):
        try:
            self.object = reading_log = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.save()
            messages.info(self.request,
                          f"書籍\"{reading_log.book}\"を登録しました")
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request,
                           f"書籍\"{reading_log.book}\"のログは登録済みです")
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "読書ログ登録"
        return context

    def get_success_url(self):
        #return reverse_lazy("reading_log:reading_log_list")
        return reverse_lazy("reading_log:individual_log", args=[self.request.user.id])


class ReadingLogUpdate(LoginRequiredMixin, generic.UpdateView):
    template_name = "reading_log/register.html"
    model = ReadingLog
    form_class = ReadingLogCreateForm

    def form_valid(self, form):
        try:
            self.object = reading_log = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.save()
            messages.info(self.request,
                          f"書籍\"{reading_log.book}\"を更新しました")
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request,
                           f"書籍\"{reading_log.book}\"のログは登録済みです")
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "読書ログ更新"
        return context

    def get_success_url(self):
        #return reverse_lazy("reading_log:reading_log_list")
        return reverse_lazy("reading_log:individual_log", args=[self.request.user.id])


class ReadingLogDelete(LoginRequiredMixin, generic.DeleteView):
    template_name = "reading_log/delete.html"
    model = ReadingLog

    def get_success_url(self):
        #return reverse_lazy("reading_log:reading_log_list")
        return reverse_lazy("reading_log:individual_log", args=[self.request.user.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "読書ログ削除確認"

        return context

    def delete(self, request, *args, **kwargs):
        self.object = reading_log = self.get_object()

        reading_log.delete()
        messages.info(self.request,
                      f"読書ログ\"{reading_log.book}\"を削除しました")
        return redirect(self.get_success_url())


class IndividualLog(LoginRequiredMixin, generic.ListView):
    template_name = "reading_log/individual_log.html"
    model = ReadingLog
    ordering = "book"
    context_object_name = "reading_log_list"
    paginate_by = 10
    pk_url_kwarg = "user_id"

    def get_queryset(self):
        page_user_id = self.kwargs.get("user_id")
        # 存在しないユーザのURLは404エラーを返す
        if not get_user_model().objects.filter(id=page_user_id).exists():
            raise Http404

        # ページユーザIDと一致するログのみ表示し、ログインユーザでなければ閲覧できない
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.id == page_user_id:
                queryset = queryset.filter(created_by=page_user_id)
            else:
                queryset = queryset.filter(created_by=page_user_id, is_public=True)
        else:
            raise Http404
        self.form = form = ReadingLogSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get("year")
            # 何も選択されていないときは0の文字列が入るため、除外
            if year and year != "0":
                queryset = queryset.filter(finish_date__year=year)

            # 何も選択されていないときは0の文字列が入るため、除外
            month = form.cleaned_data.get("month")
            if month and month != "0":
                queryset = queryset.filter(finish_date__month=month)

            # キーワードの絞り込み
            key_word = form.cleaned_data.get("key_word")
            if key_word:
                for word in key_word.split():
                    queryset = queryset.filter(
                        Q(description__icontains=word) |
                        Q(book__author__icontains=word) |
                        Q(book__title__icontains=word)).distinct()

            tag = form.cleaned_data.get("tag")
            if tag:
                queryset = queryset.filter(book__tags=tag)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_user_id = self.kwargs.get("user_id")
        page_user_name = get_user_model().objects.get(id=page_user_id).username
        print(f"page_user_id: {page_user_id}")
        print(f"page_user_name: {page_user_name}")
        context["page_user_id"] = page_user_id
        context["page_user_name"] = page_user_name
        context["search_form"] = self.form
        page: Page = context["page_obj"]
        # get_elided_page_rangeの結果を、paginator_range変数から使用可能
        context["paginator_range"] = page.paginator.get_elided_page_range(
            page.number,
            on_each_side=2,
            on_ends=1
        )

        return context


def pages2height_in_meter(num_of_pages):
    height_in_meter = num_of_pages * 0.6 * 1e-4  # 0.6 mm換算
    return round(height_in_meter, 2)


def get_height_indicator(height_in_meter):
    if 0.002 <= height_in_meter < 0.03:
        return "ミジンコ(2 mm)"
    if 0.03 <= height_in_meter < 0.08:
        return "メダカ(3 cm)"
    if 0.08 <= height_in_meter < 0.24:
        return "ハツカネズミ(8 cm)"
    elif 0.24 <= height_in_meter < 0.40:
        return "猫(24 cm)"
    elif 0.40 <= height_in_meter < 1.0:
        return "柴犬(40 cm)"
    elif 1.0 <= height_in_meter < 1.7:
        return "ニホンジカ(1 m)"
    elif 1.7 <= height_in_meter < 2.8:
        return "ホモサピエンス(1.7 m)"
    elif 2.8 <= height_in_meter < 4.53:
        return "インドゾウ(2.8 m)"
    elif 4.53 <= height_in_meter < 10:
        return "天保山(4.53 m)"
    elif 10 <= height_in_meter < 18:
        return "ジンベエザメ(10 m)"
    elif 18 <= height_in_meter < 28:
        return "ガンダム(18 m)"
    elif 28 <= height_in_meter < 131.0:
        return "シロナガスクジラ(28 m)"
    elif 131 <= height_in_meter < 300.0:
        return "京都タワー(131 m)"
    elif 300.0 <= height_in_meter < 634.0:
        return "あべのハルカス(300 m)"
    elif 634.0 <= height_in_meter < 830:
        return "東京スカイツリー(634 m)"
    elif 830 <= height_in_meter < 1337:
        return "ブルジュ・ハリファ(830 m)"
    elif 1377 <= height_in_meter < 1915:
        return "伊吹山(1377 m)"
    elif 1915 <= height_in_meter < 3776:
        return "八経ヶ岳(1915 m)"
    elif 3776 <= height_in_meter < 4478:
        return "富士山(3776 m)"
    elif 4478 <= height_in_meter < 5895:
        return "マッターホルン(4478 m)"
    elif 5895 <= height_in_meter < 8849:
        return "キリマンジャロ(5895 m)"
    elif 8849 <= height_in_meter:
        return "エベレスト(8849 m)"


def make_message(reading_log_queryset, book_status):
    book_queryset = reading_log_queryset.filter(status__status__contains=book_status)
    num_of_pages = book_queryset.aggregate(total_count=Sum("book__pages"))["total_count"]
    height_in_meter = pages2height_in_meter(num_of_pages)
    pages_indicator = get_height_indicator(height_in_meter)
    message = f"{book_status}本の高さ: {height_in_meter} m\n{pages_indicator}の大きさを超えています"
    return message


class Dashboard(LoginRequiredMixin, generic.TemplateView):
    template_name = "reading_log/dashboard.html"
    pk_url_kwarg = "user_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_user_id = self.kwargs.get("user_id")
        page_user_name = get_user_model().objects.get(id=page_user_id).username
        context["page_user_id"] = page_user_id
        context["page_user_name"] = page_user_name

        reading_log_queryset = ReadingLog.objects.all()
        if self.request.user.is_authenticated:
            if self.request.user.id == page_user_id:
                reading_log_queryset = reading_log_queryset.filter(created_by=page_user_id)
            else:
                reading_log_queryset = reading_log_queryset.filter(created_by=page_user_id, is_public=True)
        else:
            raise Http404

        # reading_log テーブルと book テーブルを結合して、ページ数を参照できるようにする
        reading_log_queryset = reading_log_queryset.select_related("book").all()
        reading_log_df = read_frame(reading_log_queryset,
                                    fieldnames=["finish_date", "book__pages"])
        none_indices = reading_log_df[reading_log_df["finish_date"].isnull()].index
        reading_log_df.drop(none_indices, inplace=True)

        # 日付カラムをdatetime化して、Y-m表記に変換
        reading_log_df["finish_date"] = pd.to_datetime(reading_log_df["finish_date"])
        reading_log_df["month"] = reading_log_df["finish_date"].dt.strftime("%Y-%m")
        # 月ごとにpivot集計
        reading_log_df = pd.pivot_table(reading_log_df, index="month", values="book__pages", aggfunc=np.sum)
        # x軸
        months_reading_log = list(reading_log_df.index.values)
        # y軸
        pages = [y[0] for y in reading_log_df.values]

        # グラフ生成
        gen = GraphGenerator()
        context["transition_plot"] = gen.transition_plot(x_books_list=months_reading_log,
                                                         y_books_list=pages)

        finished_message = make_message(reading_log_queryset, "読了")
        stacked_message = make_message(reading_log_queryset, "積読")
        context["finished_message"] = finished_message
        context["stacked_message"] = stacked_message

        return context
