from django.views.generic import DetailView, ListView

from .models import Post, PostCategory

RELATED_POSTS = 3


class PostListView(ListView):
    """Actualidad: publicaciones vigentes, filtro por categoría (?categoria=<slug>) y paginación. SEO general."""

    template_name = 'gravior/actualidad.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        self.categories = list(PostCategory.objects.filter(
            is_active=True, posts__in=Post.objects.published()).distinct())
        self.selected_category = next(
            (c for c in self.categories if c.slug == self.request.GET.get('categoria')), None)
        posts = Post.objects.published().select_related('category')
        if self.selected_category:
            posts = posts.filter(category=self.selected_category)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(post_categories=self.categories, selected_category=self.selected_category)
        return context


class PostDetailView(DetailView):
    """Detalle por slug; solo publicaciones vigentes (las demás responden 404)."""

    template_name = 'gravior/actualidad-detalle.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.published().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        related = list(Post.objects.published().filter(category=post.category).exclude(pk=post.pk)
                       .select_related('category')[:RELATED_POSTS])
        if len(related) < RELATED_POSTS:
            related += list(Post.objects.published().exclude(pk__in=[post.pk, *[p.pk for p in related]])
                            .select_related('category')[:RELATED_POSTS - len(related)])
        context.update(
            related_posts=related,
            post_categories=PostCategory.objects.filter(is_active=True, posts__in=Post.objects.published()).distinct(),
            seo_title=post.seo_title or post.title,
            seo_description=post.seo_description or post.excerpt,
            share_url=self.request.build_absolute_uri(post.get_absolute_url()),
        )
        return context
