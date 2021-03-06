from django.db.models import Count
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.utils.log import getLogger
from taggit.models import Tag
from .models import Category, Post, Comment
from .forms import CommentForm

logger = getLogger('zhiwehu.logfile')

class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        post_list = Post.objects.filter(published=True)

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
        logger.debug('self.year = %s' % self.year)
        if self.year:
            post_list = post_list.filter(created__year=self.year)

        self.month = self.kwargs.get('month', None)
        logger.debug('self.month = %s' % self.month)
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
        context['month_list'] = Post.objects.extra({'date_created': 'LAST_DAY(created)'}).filter(published=True).values(
            'date_created').annotate(
            post_count=Count('id'))[:12]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug', None)
        if slug:
            post = get_object_or_404(Post, slug=slug)
            post.view_count = post.view_count + 1
            post.save()
            return post
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['month_list'] = Post.objects.extra({'date_created': 'LAST_DAY(created)'}).filter(published=True).values(
            'date_created').annotate(
            post_count=Count('id'))[:12]
        return context


@require_http_methods(['POST'])
def add_comment(request):
    post = None
    post_id = int(request.POST.get('post_id', -1))
    if post_id:
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            pass

    if post == None:
        return JsonResponse({'status': 'error', 'message': _(u'the post does not exist')})

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post

        if request.user.is_authenticated():
            comment.user = request.user
            comment.user_name = request.user.username
            comment.user_email = request.user.email
            comment.user_website = request.user.website

        parent = None
        parent_id = request.POST.get('parent_id', None)
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
            except Exception:
                pass
        comment.parent = parent

        if comment.user and comment.user.is_staff:
            comment.approved = True
        comment.save()
        return JsonResponse(comment.json)
    else:
        return JsonResponse({'status': 'error', 'message': _(u'post data error')})
