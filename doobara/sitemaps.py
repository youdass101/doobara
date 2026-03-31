from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from shop.models import Categorie, Product


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["index", "shop", "contactus", "blog", "single_blog_post"]

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return (
            Categorie.objects.filter(products__active=True)
            .distinct()
            .order_by("name")
        )

    def location(self, item):
        return reverse("filtering", kwargs={"locat": item.name})


class ProductSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Product.objects.filter(active=True).order_by("name")

    def location(self, item):
        return reverse("single_product_by_slug", kwargs={"slug": item.slug})

    def lastmod(self, item):
        return item.updated_time
