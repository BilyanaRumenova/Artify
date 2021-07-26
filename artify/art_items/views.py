from django.shortcuts import render, redirect

from artify.art_items.forms import ArtItemForm, EditArtItemForm, CommentForm
from artify.art_items.models import ArtItem, Like


def list_items(request):
    all_items = ArtItem.objects.all()
    context = {
        'art_items': all_items
    }
    return render(request, 'art_items/items_list.html', context)


def create_item(request):
    if request.method == 'POST':
        form = ArtItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = ArtItemForm()

    context = {
        'form': form,
    }
    return render(request, 'art_items/item_create.html', context)


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


def delete_item(request,pk):
    item = ArtItem.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('list items')
    else:
        context = {
            'item': item
        }
        return render(request, 'art_items/item_delete.html', context)


def item_details(request, pk):
    item = ArtItem.objects.get(pk=pk)
    item.likes_count = item.like_set.count()

    # is_liked_by_user = item.like_set.filter(user_id=request.user.id).exists()

    context = {
        'item': item,
        'comment_form': CommentForm(
            initial={
                'item_pk': pk,
            }
        ),
        'comments': item.comment_set.all(),
    }

    return render(request, 'art_items/item-details.html', context)


def like_item(request, pk):
    item_to_like = ArtItem.objects.get(pk=pk)
    # like_object_by_user = item_to_like.like_set.filter()

    like = Like(
        art_item=item_to_like,
    )
    like.save()
    return redirect('item details', item_to_like.id)


def comment_item(request, pk):
    item = ArtItem.objects.get(pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.save()

    return redirect('item details', item.id)


