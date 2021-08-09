from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


from artify.art_items.forms import ArtItemForm, CommentForm
from artify.art_items.models import ArtItem, Like, Comment

from django.views import generic as views


class ItemsListView(LoginRequiredMixin, views.ListView):
    model = ArtItem
    template_name = 'art_items/items_list.html'
    context_object_name = 'art_items'


class CreateItemView(LoginRequiredMixin, views.CreateView):
    model = ArtItem
    form_class = ArtItemForm
    template_name = 'art_items/item_create.html'
    success_url = reverse_lazy('list items')

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

    def get_success_url(self):
        url = reverse_lazy('item details', kwargs={'pk': self.object.id})
        return url


class DeleteItemView(LoginRequiredMixin, views.DeleteView):
    model = ArtItem
    template_name = 'art_items/item_delete.html'
    success_url = reverse_lazy('list items')

    def dispatch(self, request, *args, **kwargs):
        art_item = self.get_object()
        if not art_item.user_id == request.user.id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ItemDetailsView(LoginRequiredMixin, views.DetailView):
    model = ArtItem
    template_name = 'art_items/item-details.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = context['item']

        context['comment_form'] = CommentForm(initial={'item_pk': item.id, })
        context['comments'] = item.comment_set.all()
        context['is_liked'] = item.like_set.filter(user_id=self.request.user.id).exists()
        context['is_owner'] = item.user == self.request.user

        return context


class LikeItemView(LoginRequiredMixin, views.View):
    def get(self, request, *args, **kwargs):
        item_to_like = ArtItem.objects.get(pk=self.kwargs['pk'])
        like_object_by_user = item_to_like.like_set.filter(user_id=self.request.user.id).first()

        if like_object_by_user:
            like_object_by_user.delete()
        else:
            like = Like(
                item=item_to_like,
                user=self.request.user,
            )
            like.save()
        return redirect('item details', item_to_like.id)


class CommentItemView(LoginRequiredMixin, views.FormView):
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.item = ArtItem.objects.get(pk=self.kwargs['pk'])
        comment.user = self.request.user
        comment.save()
        return redirect('item details', self.kwargs['pk'])


class PhotographyItemsListView(LoginRequiredMixin, views.ListView):
    model = ArtItem
    template_name = 'categories/photography_list_items.html'
    context_object_name = 'photography_items'

    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)

        photography_items = ArtItem.objects.filter(type='photography')
        context = {
            'photography_items': photography_items
        }
        return context


class PaintingsListView(LoginRequiredMixin, views.ListView):
    model = ArtItem
    template_name = 'categories/paintings_list_items.html'
    context_object_name = 'painting_items'

    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)

        painting_items = ArtItem.objects.filter(type='painting')
        context = {
            'painting_items': painting_items
        }
        return context


class PortraitsListView(LoginRequiredMixin, views.ListView):
    model = ArtItem
    template_name = 'categories/portrait_list_items.html'
    context_object_name = 'portrait_items'

    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)

        portrait_items = ArtItem.objects.filter(type='portrait')
        context = {
            'portrait_items': portrait_items
        }
        return context


class FashionItemsListView(LoginRequiredMixin, views.ListView):
    model = ArtItem
    template_name = 'categories/fashion_items_list_view.html'
    context_object_name = 'fashion_items'

    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)

        fashion_items = ArtItem.objects.filter(type='fashion')
        context = {
            'fashion_items': fashion_items
        }
        return context

# def photography_list_items(request, **kwargs):
#     photography_items = ArtItem.objects.filter(type='photography')
#     context = {
#         'photography_items': photography_items
#     }
#     return render(request, 'categories/photography_list_items.html', context)


# def list_items(request):
#     all_items = ArtItem.objects.all()
#     context = {
#         'art_items': all_items
#     }
#     return render(request, 'art_items/items_list.html', context)

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





