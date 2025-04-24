from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, DeleteView
from blog.forms import PostForm, CommentForm
from blog.models import Post, Category


def index(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    cat = Category.objects.all()
    return render(request, 'blog/index.html', {'posts': posts, 'cat': cat})


def post_detail(request, slug_name):
    post = get_object_or_404(Post, slug=slug_name, is_published=True)
    viewed_posts = request.session.get('viewed_posts', [])

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', slug_name=post.slug)
    else:
        form = CommentForm()

    if slug_name not in viewed_posts:
        post.views += 1
        post.save(update_fields=['views'])
        viewed_posts.append(slug_name)
        request.session['viewed_posts'] = viewed_posts

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments': post.comments.all()})


class UpdatePage(UpdateView):
    model = Post
    fields = ['title', 'content', 'category', 'photo', 'is_published', 'slug']
    template_name = 'blog/edit_page.html'
    success_url = reverse_lazy('home')


class AddPost(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blog/add_post.html'
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.auther = self.request.user
        return super().form_valid(form)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'blog/add_post.html', {'form': form})


@login_required
def about(request):
    posts = Post.objects.all()
    list_post_user = []
    for i in posts:
        if request.user == i.auther:
            list_post_user.append(i)
    return render(request, 'blog/about.html', {'posts': list_post_user})


class DeletePost(DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('about')


def add_article(request):
    return render(request, 'blog/add_article.html')


def register(request):
    return render(request, 'blog/register.html')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Надо быть веселым</h1>")
