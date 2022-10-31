from django.core.paginator import Paginator


def pagination(request, post):
    amount_posts_on_page = 10
    paginator = Paginator(post, amount_posts_on_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
