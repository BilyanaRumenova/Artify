from django.urls import path

from artify.art_items.views import CreateItemView, ItemsListView, UpdateItemView, DeleteItemView, \
    ItemDetailsView, LikeItemView, CommentItemView, PhotographyItemsListView, PaintingsListView, PortraitsListView, \
    FashionItemsListView, home_page

urlpatterns = (
    path('', ItemsListView.as_view(), name='list items'),
    path('create/', CreateItemView.as_view(), name='create item'),
    path('edit/<int:pk>', UpdateItemView.as_view(), name='edit item'),
    path('delete/<int:pk>', DeleteItemView.as_view(), name='delete item'),
    path('details/<int:pk>', ItemDetailsView.as_view(), name='item details'),
    path('like/<int:pk>', LikeItemView.as_view(), name='like item'),
    path('comment/<int:pk>', CommentItemView.as_view(), name='comment item'),
    path('photography/', PhotographyItemsListView.as_view(), name='photography items'),
    path('paintings/', PaintingsListView.as_view(), name='painting items'),
    path('portraits/', PortraitsListView.as_view(), name='portrait items'),
    path('fashion/', FashionItemsListView.as_view(), name='fashion items'),
    path('home/', home_page, name='home'),
)
