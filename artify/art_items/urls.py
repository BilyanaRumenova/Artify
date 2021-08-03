from django.urls import path

from artify.art_items.views import CreateItemView, ItemsListView, UpdateItemView, DeleteItemView, \
    ItemDetailsView, LikeItemView, CommentItemView

urlpatterns = (
    # path('', list_items, name='list items'),
    path('', ItemsListView.as_view(), name='list items'),
    # path('create/', create_item, name='create item'),
    path('create/', CreateItemView.as_view(), name='create item'),
    # path('edit/<int:pk>', edit_item, name='edit item'),
    path('edit/<int:pk>', UpdateItemView.as_view(), name='edit item'),
    # path('delete/<int:pk>', delete_item, name='delete item'),
    path('delete/<int:pk>', DeleteItemView.as_view(), name='delete item'),
    # path('details/<int:pk>', item_details, name='item details'),
    path('details/<int:pk>', ItemDetailsView.as_view(), name='item details'),
    # path('like/<int:pk>', like_item, name='like item'),
    path('like/<int:pk>', LikeItemView.as_view(), name='like item'),
    # path('comment/<int:pk>', comment_item, name='comment item'),
    path('comment/<int:pk>', CommentItemView.as_view(), name='comment item'),
)