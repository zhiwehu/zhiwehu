from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.views.generic import ListView, DetailView

from .models import Category, Post
from taggit.models import Tag


class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 3

    def get_queryset(self):
        post_list = Post.objects.all()

        self.category = None
        category_slug = self.kwargs.get('category', None)
        if category_slug:
            try:
                self.category = Category.objects.get(slug=category_slug)
            except Category.DoesNotExist:
                self.category = None
        if self.category:
            post_list = post_list.filter(category=self.category)

        self.tag = None
        tag = self.kwargs.get('tag', None)
        if tag:
            try:
                self.tag = Tag.objects.get(slug=tag)
            except Tag.DoesNotExist:
                self.tag = None
        if self.tag:
            post_list = post_list.filter(tags__in=[self.tag])

        self.year = self.kwargs.get('year', None)
        if self.year:
            post_list = post_list.filter(created__year=self.year)

        self.month = self.kwargs.get('month', None)
        if self.month:
            post_list = post_list.filter(created__month=self.month)

        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['category'] = self.category
        context['tags'] = Tag.objects.all()
        context['tag'] = self.tag
        context['year'] = self.year
        context['month'] = self.month
        context['month_list'] = Post.objects.extra({'date_created': 'date(created)'}).values('date_created').annotate(
            post_count=Count('id'))[:12]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug', None)
        if slug:
            return get_object_or_404(Post, slug=slug)
        raise Http404