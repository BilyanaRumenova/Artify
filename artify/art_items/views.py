from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from artify.art_items.forms import ArtItemForm, EditArtItemForm, CommentForm
from artify.art_items.models import ArtItem, Like, Comment

from django.views import generic as views
from django.views.generic.detail import SingleObjectMixin


class ItemsListView(views.ListView):
    model = ArtItem
    template_name = 'art_items/items_list.html'
    context_object_name = 'art_items'


class CreateItemView(LoginRequiredMixin, views.CreateView):
    model = ArtItem
    template_name = 'art_items/item_create.html'
    form_class = ArtItemForm
    context_object_name = 'art_item'
    # success_url = reverse_lazy('list items')

    def get_success_url(self):
        url = reverse_lazy('item details', kwargs={'pk': self.object.id})
        return url

    def form_valid(self, form):
        art_item = form.save(commit=False)
        art_item.user = self.request.user
        art_item.save()
        return super().form_valid(form)


class UpdateItemView(LoginRequiredMixin, views.UpdateView):
    model = ArtItem
    template_name = 'art_items/item_edit.html'
    form_class = ArtItemForm

    def dispatch(self, request, *args, **kwargs):
        art_item = self.get_object()
        if not art_item.user_id == request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    # def get_success_url(self):
    #     url = reverse_lazy('item details', kwargs={'pk': self.object.id})
    #     return url


class DeleteItemView(LoginRequiredMixin, views.DeleteView):
    model = ArtItem
    template_name = 'art_items/item_delete.html'
    success_url = reverse_lazy('list items')

    def dispatch(self, request, *args, **kwargs):
        art_item = self.get_object()
        if not art_item.user_id == request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ItemDetailsView(views.DetailView):
    model = ArtItem
    template_name = 'art_items/item-details.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        context['comment_form'] = CommentForm(initial={'item_pk': item.id,})
        context['comments'] = item.comment_set.all()
        context['is_liked'] = item.like_set.filter(user_id=self.request.user.id).exists()
        context['is_owner'] = item.user == self.request.user

        return context


class LikeItemView(LoginRequiredMixin, views.View):
    def get(self, request, **kwargs):
        item_to_like = ArtItem.objects.get(pk=self.kwargs['pk'])
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


class CommentItemView(LoginRequiredMixin, views.FormView):
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.item = ArtItem.objects.get(pk=self.kwargs['pk'])
        comment.user = self.request.user
        comment.save()
        return redirect('item details', self.kwargs['pk'])


# @login_required
# def like_item(request, pk):
#     item_to_like = ArtItem.objects.get(pk=pk)
#     like_object_by_user = item_to_like.like_set.filter(user_id=request.user.id).first()
#
#     if like_object_by_user:
#         like_object_by_user.delete()
#     else:
#         like = Like(
#             item=item_to_like,
#             user=request.user,
#         )
#         like.save()
#     return redirect('item details', item_to_like.id)
#

# @login_required
# def comment_item(request, pk):
#     item = ArtItem.objects.get(pk=pk)
#     form = CommentForm(request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.user = request.user
#         comment.save()
#
#     return redirect('item details', item.id)


# def list_items(request):
#     all_items = ArtItem.objects.all()
#     context = {
#         'art_items': all_items
#     }
#     return render(request, 'art_items/items_list.html', context)


# @login_required
# def create_item(request):
#     if request.method == 'POST':
#         form = ArtItemForm(request.POST, request.FILES)
#         if form.is_valid():
#             art_item = form.save(commit=False)
#             art_item.user = request.user
#             art_item.save()
#             return redirect('list items')
#
#     else:
#         form = ArtItemForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'art_items/item_create.html', context)

# @login_required
# def edit_item(request, pk):
#     item = ArtItem.objects.get(pk=pk)
#     if request.method == 'POST':
#         form = EditArtItemForm(request.POST, request.FILES, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('list items')
#     else:
#         form = EditArtItemForm(instance=item)
#
#     context = {
#         'form': form,
#         'item': item,
#     }
#     return render(request, 'art_items/item_edit.html', context)

# @login_required
# def delete_item(request, pk):
#     item = ArtItem.objects.get(pk=pk)
#     if request.method == 'POST':
#         item.delete()
#         return redirect('list items')
#     else:
#         context = {
#             'item': item
#         }
#         return render(request, 'art_items/item_delete.html', context)


# def item_details(request, pk):
# #     item = ArtItem.objects.get(pk=pk)
# #     item.likes_count = item.like_set.count()
# #     is_liked_by_user = item.like_set.filter(user_id=request.user.id).exists()
# #
# #     context = {
# #         'item': item,
# #         'comment_form': CommentForm(
# #             initial={
# #                 'item_pk': pk,
# #             }
# #         ),
# #         'comments': item.comment_set.all(),
# #         'is_liked': is_liked_by_user,
# #     }
# #
# #     return render(request, 'art_items/item-details.html', context)





