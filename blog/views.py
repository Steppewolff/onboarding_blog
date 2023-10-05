from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic import DetailView
from .forms import PostForm
from django.utils import timezone
from .models import Post

# Create your views here.

# Class based views


# class CountriesFeedView(ListView): ######¿esta forma de explicitar el modelo en la clase es mejor que la de abajo?¿En la de abajo no
# hace falta porque se pasa Post. objects.all en la variable queryset?
#     template_name = 'countries/feed.html'
#     model = Country
#     paginate_by = 10
#     context_object_name = 'countries'  -->  Este es el nombre del objeto en la plantilla, se refiere a un objeto concreto?

class PostListView(ListView):
    queryset = Post.objects.all()
    template_name = 'post_list.html'
    paginate_by = 10


    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.order_by("published_date")

        return qs

class PostDetailView(DetailView):
    queryset = Post.objects.all()
    template_name = 'post_detail.html'

    # def get_context_data(self, **kwargs):
    #     # qs = super().get_queryset(*args, **kwargs)
    #     pk = self.kwargs['pk']

    #     print('pk: ', pk)
    #     print('Post: ', Post)

    #     post = get_object_or_404(Post, pk=pk)

    #     print('post: ', post)

    #     return post
    
    #¿Es necesario pasar aqui **kwargs para usarlo debajo o pasa por defecto?
    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=pk)

        # return post
        return Post.objects.filter(pk=pk)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
 