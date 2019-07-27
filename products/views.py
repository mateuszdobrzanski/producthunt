from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Upvote, Comment
from django.utils import timezone


def home(request):
    products = Product.objects.all()
    return render(request,
                  'products/home.html',
                  {'products': products})


@login_required(login_url="/accounts/login")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']

            # checking if url starts with https or http prefix
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']

            # set current time on promotion
            product.pub_date = timezone.datetime.now()

            # get current username for occasion
            product.hunter = request.user

            # -----save to database
            product.save()

            # return user to the product detail web page
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All fields are required'})
    else:
        return render(request, 'products/create.html')


# Show product details and comments
def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comments = Comment.objects.filter(product_id=product_id)
    return render(request, 'products/detail.html', {'product': product,
                                                    'comments': comments})


@login_required(login_url="/accounts/login")
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        upvotes = Upvote.objects.all()
        for upvote in upvotes:
            if upvote.product == product and upvote.voter == request.user:
                return redirect('/products/' + str(product.id))
        # will only get her if there is no match inside the loop
        new_upvote = Upvote()
        new_upvote.product = product
        new_upvote.voter = request.user
        new_upvote.save()
        return redirect('/products/' + str(product.id))


@login_required(login_url="/accounts/login")
def add_comment(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        user = request.user
        comment_body = request.POST['comment_body']
        pub_date = timezone.datetime.now()

        comment = Comment()
        comment.product = product
        comment.user = user
        comment.comment_body = comment_body
        comment.pub_date = pub_date
        comment.save()

        return redirect('/products/' + str(product.id))
