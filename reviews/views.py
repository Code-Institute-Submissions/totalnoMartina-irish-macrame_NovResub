from django.shortcuts import render, redirect, get_object_or_404
from .models import Macrame, Review
from .forms import ReviewForm


def macrames(request):
    """ Rendering products of macrames to be able to manipulate reviews connected to macrames """
    macrame_ = Macrame.objects.all()
    context = {
        'macrame_': macrame_,

    }
    return render(request, 'shoppingapp/macrame-detail.html', context)


def create_review(request, pk):
    """ Creating a review """
    form = ReviewForm(initial={'product_reviewed': pk, 'user_reviewing': request.user})
    macrame = get_object_or_404(Macrame, pk=pk)
    context = {
        'form': form,
        'macrame': macrame,
    }
    if request.method == 'POST':
        print('Printing Post:', request.POST)
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('macrame-detail', macrame_id=pk)

    return render(request, 'reviews/reviews.html', context)


def update_review(request, pk):
    """ A view to update review """

    review = Review.objects.get(id=pk)

    form = ReviewForm(instance=review)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'reviews/reviews.html', context)


def delete_review(request, pk):
    """ A view to delete reviews """
    review = Review.objects.get(id=pk)
    form = ReviewForm(instance=review)

    context = {
        # 'form': form,
        'item': review,
    }

    if request.method == 'POST':
        review.delete()
        return redirect('/')

    return render(request, 'reviews/delete_review.html', context)
