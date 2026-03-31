
from . import views
from django.urls import path

# is list
# contain the website directory and functionality site network map
urlpatterns=[
    # Index page or Home page 
    path("", views.index, name="index"),
    # Shop page for all products 
    path("shop", views.shop, name="shop"),
    # Shop page filtering product subpage
    path("shop/<str:locat>/", views.filtering, name="filtering"),
    # Contact Us page request
    path("contactus", views.contactus, name="contactus"),
    # Canonical single product page request (slug-based)
    path("products/<slug:slug>/", views.single_product, name="single_product_by_slug"),
    # Backward-compatible legacy product path (name-based)
    path('single_product/<str:locat>/', views.single_product, name="single_product"),
    # search keyword request
    path('search', views.search, name="search"),
    # order list filter request
    path("orderby", views.orderby, name="orderby"),
    # Internal product feed export (JSON) for Merchant/Meta mapping QA.
    path("internal/exports/products.json", views.internal_product_feed_export, name="internal_product_feed_export"),
    # NEW: Live Google Merchant Center CSV feed endpoint.
    path("google-product-feed.csv", views.google_product_feed_csv, name="google_product_feed_csv"),
    # NEW: Live Meta Commerce Manager CSV feed endpoint.
    path("meta-catalog-feed.csv", views.meta_catalog_feed_csv, name="meta_catalog_feed_csv"),
]
