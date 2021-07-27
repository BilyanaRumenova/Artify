from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from artify.art_items.forms import ArtItemForm, EditArtItemForm, CommentForm
from artify.art_items.models import ArtItem, Like


def list_items(request):
    all_items = ArtItem.objects.all()
    context = {
        'art_items': all_items
    }
    return render(request, 'art_items/items_list.html', context)


@login_required
def create_item(request):
    if request.method == 'POST':
        form = ArtItemForm(request.POST, request.FILES)
        if form.is_valid():
            art_item = form.save(commit=False)
            art_item.user = request.user
            art_item.save()
            return redirect('list items')

    else:
        form = ArtItemForm()

    context = {
        'form': form,
    }
    return render(request, 'art_items/item_create.html', context)


@login_required
def edit_item(request, pk):
    item = ArtItem.objects.get(pk=pk)
    if request.method == 'POST':
        form = EditArtItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('list items')
    else:
        form = EditArtItemForm(instance=item)

    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'art_items/item_edit.html', context)


@login_required
def delete_item(request, pk):
    item = ArtItem.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('list items')
    else:
        context = {
            'item': item
        }
        return render(request, 'art_items/item_delete.html', context)


@login_required
def like_item(request, pk):
    item_to_like = ArtItem.objects.get(pk=pk)
    like_object_by_user = item_to_like.like_set.filter(user_id=request.user.id).first()

    if like_object_by_user:
        like_object_by_user.delete()
    else:
        like = Like(
            item=item_to_like,
            user=request.user,
        )
        like.save()
    return redirect('item details', item_to_like.id)


@login_required
def comment_item(request, pk):
    item = ArtItem.objects.get(pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()

    return redirect('item details', item.id)


def item_details(request, pk):
    item = ArtItem.objects.get(pk=pk)
    item.likes_count = item.like_set.count()
    is_liked_by_user = item.like_set.filter(user_id=request.user.id).exists()

    context = {
        'item': item,
        'comment_form': CommentForm(
            initial={
                'item_pk': pk,
            }
        ),
        'comments': item.comment_set.all(),
        'is_liked': is_liked_by_user,
    }

    return render(request, 'art_items/item-details.html', context)



