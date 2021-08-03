from django.urls import path

from artify.art_items.views import edit_item, like_item, comment_item, \
    delete_item, ItemCreateView, ItemsListView, item_details

urlpatterns = (
    # path('', list_items, name='list items'),
    path('', ItemsListView.as_view(), name='list items'),
    # path('create/', create_item, name='create item'),
    path('create/', ItemCreateView.as_view(), name='create item'),
    path('edit/<int:pk>', edit_item, name='edit item'),
    path('delete/<int:pk>', delete_item, name='delete item'),
    path('details/<int:pk>', item_details, name='item details'),
    # path('details/<int:pk>', ItemDetailsView.as_view(), name='item details'),
    path('like/<int:pk>', like_item, name='like item'),
    path('comment/<int:pk>', comment_item, name='comment item'),
)