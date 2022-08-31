from comments_app.forms import FormComment
from comments_app.models import Comment
from django.contrib import messages
from django.db.models import Case, Count, Q, When
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .models import Post


class PostIndex(ListView):
    model = Post
    template_name = 'posts_app/index.html'
    paginate_by = 6
    context_object_name = 'posts'  # não entendi de onde vem esse "posts"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id').filter(post_published=True)
        qs = qs.annotate(
            comment_number=Count(
                Case(
                    When(comment__comment_published=True, then=1)
                )
            )
        )
        return qs


class PostSearch(PostIndex):
    template_name = 'posts_app/search_post.html'

    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get('term')

        if not term:
            return qs

        qs = qs.filter(
            Q(post_title__icontains=term) |
            Q(post_author__first_name__iexact=term) |
            Q(post_content__icontains=term) |
            Q(post_resume__icontains=term) |
            Q(post_category__category_name__iexact=term)
        )

        return qs


class PostCategory(PostIndex):
    template_name = 'posts_app/category_post.html'

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.kwargs.get('category', None)

        qs = qs.filter(post_category__category_name__iexact=category)
        return qs


class PostDetails(UpdateView):
    template_name = 'posts_app/detail_post.html'
    model = Post
    form_class = FormComment
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = Comment.objects.filter(
            comment_published=True,
            comment_post=post.id,
        )
        context['comments'] = comments

        return context

    def form_valid(self, form):
        post = self.get_object()
        comment = Comment(**form.cleaned_data)
        comment.comment_post = post

        if self.request.user.is_authenticated:
            comment.comment_user = self.request.user

        comment.save()
        messages.success(self.request, 'Comentário enviado com sucesso!')
        return redirect('detail_post', pk=post.id)
