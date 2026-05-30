from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Post, Categoria

def blog(request, template_name='blog/blog.html'):
    posts = Post.objects.filter(publicado=True).order_by('-publicado_en')
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')
    query = request.GET.get('query', '')

    if query:
        posts = posts.filter(
            Q(titulo__icontains=query) |
            Q(contenido1__icontains=query)
        ).distinct()

    context = {
        'posts': posts,           # ← plural, consistente con el template
        'categorias': categorias,
        'categoria_seleccionada': None,
        'query': query,
    }
    return render(request, template_name, context)

def categoria(request, categoria_slug):
    categoria_obj = get_object_or_404(Categoria, slug=categoria_slug, activo=True)
    posts = Post.objects.filter(categoria=categoria_obj, publicado=True).order_by('-publicado_en')
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')

    context = {
        'posts': posts,
        'categorias': categorias,
        'categoria_seleccionada': categoria_obj,
    }
    return render(request, 'blog/blog.html', context)

def post(request, post_id):
    post_obj = get_object_or_404(Post, id=post_id, publicado=True)
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')

    # Último post (excluyendo el actual)
    ultimo_post = Post.objects.filter(
        publicado=True
    ).exclude(id=post_id).order_by('-publicado_en').first()

    # Posts relacionados por categoría (excluyendo el actual)
    categorias_del_post = post_obj.categoria.all()
    recomendados = Post.objects.filter(
        publicado=True,
        categoria__in=categorias_del_post
    ).exclude(id=post_id).distinct().order_by('-publicado_en')[:2]

    if recomendados.count() < 2:
        recomendados = Post.objects.filter(
            publicado=True
        ).exclude(id=post_id).order_by('-publicado_en')[:2]

    # ↓ ESTO ES LO NUEVO — artículos relacionados para la sección de abajo
    posts_relacionados = Post.objects.filter(
        publicado=True,
        categoria__in=categorias_del_post
    ).exclude(id=post_id).distinct().order_by('-publicado_en')[:12]

    # Si no hay de la misma categoría, trae los más recientes
    if not posts_relacionados.exists():
        posts_relacionados = Post.objects.filter(
            publicado=True
        ).exclude(id=post_id).order_by('-publicado_en')[:12]

    context = {
        'post': post_obj,
        'categorias': categorias,
        'ultimo_post': ultimo_post,
        'recomendados': recomendados,
        'posts_relacionados': posts_relacionados,  # ← nuevo
    }
    return render(request, 'blog/post.html', context)

def ultimo_post(request):
    ultimo = Post.objects.filter(publicado=True).order_by('-publicado_en').first()
    if ultimo:
        return redirect('blog:post', post_id=ultimo.id)
    return redirect('blog:blog')