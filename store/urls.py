from django.urls import path
from . import views


urlpatterns = [
    path("products/",views.product_list, name="product_list"),
    path("product/<int:id>/",views.product_details, name="product_details"),
    path("product/add/",views.add_product,name="add_product"),
    path("product/<int:id>/edit/", views.edit_product, name="edit_product"),
    path("product/<int:id>/delete/", views.delete_product, name="delete_product"),
    path("session_test/",views.session_test, name="session_test"),
    path("session-view/", views.session_view, name="session_view"),
    path("delete-session/", views.delete_session, name="delete_session"),
    path("cart/add/<int:id>/",views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("cart/remove/<int:id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/increase/<int:id>/", views.increase_quantity, name="increase_quantity"),
    path("cart/decrease/<int:id>/", views.decrease_quantity, name="decrease_quantity"),
    path("cart/checkout/",views.checkout, name="checkout"),
    path("order_confirmation/<int:order_id>/", views.order_confirmation, name="order_confirmation"),
    path("my_orders/", views.my_orders, name="my_orders"),
    path("login/",views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]