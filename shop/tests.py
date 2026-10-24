import csv
import io

from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.test import TestCase, override_settings

from .admin import ProductImageInlineForm, ProductImageInlineFormSet
from .models import Categorie, MediaAsset, Product, ProductImage, ProductVariant


@override_settings(SECURE_SSL_REDIRECT=False, ALLOWED_HOSTS=["testserver"])
class InternalProductFeedExportTests(TestCase):
    def setUp(self):
        self.camera_category = Categorie.objects.create(
            name="CCTV Camera",
            description="Security camera products",
        )
        self.product = Product.objects.create(
            name="Feed Ready Camera",
            price="149.99",
            currency="USD",
            active=True,
            quantity=3,
            availability="in stock",
            brand="Doobara",
            sku="CAM-001",
        )
        self.product.category.add(self.camera_category)

    def test_internal_feed_export_contains_required_fields(self):
        response = self.client.get("/internal/exports/products.json")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertIn("fields", payload)
        self.assertIn("products", payload)
        self.assertEqual(
            payload["fields"],
            [
                "id",
                "title",
                "description",
                "url",
                "image_url",
                "price",
                "currency",
                "availability",
                "brand",
                "sku",
                "condition",
                "product_type",
                "google_product_category",
                "meta_fb_product_category",
            ],
        )

        product_row = payload["products"][0]
        self.assertEqual(product_row["id"], str(self.product.id))
        self.assertEqual(product_row["title"], self.product.name)
        self.assertEqual(product_row["currency"], "USD")
        self.assertEqual(product_row["availability"], "in stock")
        self.assertEqual(product_row["condition"], "new")
        self.assertEqual(product_row["product_type"], "CCTV Camera")
        self.assertEqual(
            product_row["google_product_category"],
            "Electronics > Video > Video Cameras",
        )
        self.assertEqual(
            product_row["meta_fb_product_category"],
            "Electronics > Cameras",
        )
        self.assertIn("/products/", product_row["url"])
        self.assertTrue(product_row["url"].startswith("http://testserver/"))

    def test_internal_feed_export_image_url_is_null_safe(self):
        response = self.client.get("/internal/exports/products.json")
        product_row = response.json()["products"][0]
        self.assertIsNone(product_row["image_url"])

        ProductImage.objects.create(
            product=self.product,
            image="static/doobarashop/upload/images/feed-image.jpg",
            thumbnail=True,
        )
        response_with_image = self.client.get("/internal/exports/products.json")
        product_row_with_image = response_with_image.json()["products"][0]
        self.assertIn("http://testserver/", product_row_with_image["image_url"])

    def test_internal_feed_export_exposes_missing_fields(self):
        response = self.client.get("/internal/exports/products.json")
        product_row = response.json()["products"][0]
        self.assertNotIn("condition", product_row["missing_fields"])

    def test_internal_feed_export_surfaces_unmapped_category_gaps(self):
        unmapped_category = Categorie.objects.create(
            name="Custom Bundle",
            description="Internal-only grouping",
        )
        unmapped_product = Product.objects.create(
            name="Unmapped Product",
            price="299.99",
            currency="USD",
            active=True,
            quantity=5,
            availability="in stock",
        )
        unmapped_product.category.add(unmapped_category)

        response = self.client.get("/internal/exports/products.json")
        readiness_gaps = response.json()["readiness_gaps"]

        self.assertIn("manual_category_mapping_products", readiness_gaps)
        self.assertIn("manual_category_mapping_product_types", readiness_gaps)
        self.assertIn("Custom Bundle", readiness_gaps["manual_category_mapping_product_types"])


@override_settings(SECURE_SSL_REDIRECT=False, ALLOWED_HOSTS=["testserver"])
class MetaCatalogFeedCsvTests(TestCase):
    def test_media_asset_meta_image_is_feed_only(self):
        product = Product.objects.create(
            name="Product With Reusable Meta Creative",
            price="49.99",
            currency="USD",
            active=True,
            quantity=1,
            availability="in stock",
        )
        ProductImage.objects.create(
            product=product,
            image="products/images/storefront.jpg",
            thumbnail=True,
        )
        meta_asset = MediaAsset.objects.create(
            file="product_media/meta-creative.jpg",
            alt_text="Catalog-only creative",
        )
        ProductImage.objects.create(
            product=product,
            asset=meta_asset,
            meta_image=True,
        )

        response = self.client.get("/meta-catalog-feed.csv")
        rows = list(csv.DictReader(io.StringIO(response.content.decode("utf-8"))))
        product_row = next(row for row in rows if row["id"] == str(product.id))
        storefront_product = product.serialize("all")

        self.assertTrue(
            product_row["image_link"].endswith("/product_media/meta-creative.jpg")
        )
        self.assertTrue(
            storefront_product["main_image"]["url"].endswith(
                "/products/images/storefront.jpg"
            )
        )
        self.assertNotIn(
            "/product_media/meta-creative.jpg",
            [image["url"] for image in storefront_product["all_images"]],
        )

    def test_meta_catalog_feed_prefers_selected_meta_image(self):
        product = Product.objects.create(
            name="Product With Meta Creative",
            price="49.99",
            currency="USD",
            active=True,
            quantity=1,
            availability="in stock",
        )
        ProductImage.objects.create(
            product=product,
            image="products/images/storefront.jpg",
            thumbnail=True,
        )
        ProductImage.objects.create(
            product=product,
            image="products/images/meta-ad.jpg",
            meta_image=True,
        )

        response = self.client.get("/meta-catalog-feed.csv")
        rows = list(csv.DictReader(io.StringIO(response.content.decode("utf-8"))))
        product_row = next(row for row in rows if row["id"] == str(product.id))

        self.assertTrue(product_row["image_link"].endswith("/products/images/meta-ad.jpg"))
        self.assertIn("/products/images/storefront.jpg", product_row["additional_image_link"])

    def test_meta_catalog_feed_falls_back_to_thumbnail(self):
        product = Product.objects.create(
            name="Product Without Meta Creative",
            price="49.99",
            currency="USD",
            active=True,
            quantity=1,
            availability="in stock",
        )
        ProductImage.objects.create(
            product=product,
            image="products/images/storefront.jpg",
            thumbnail=True,
        )

        response = self.client.get("/meta-catalog-feed.csv")
        rows = list(csv.DictReader(io.StringIO(response.content.decode("utf-8"))))
        product_row = next(row for row in rows if row["id"] == str(product.id))

        self.assertTrue(product_row["image_link"].endswith("/products/images/storefront.jpg"))

    def test_meta_catalog_feed_falls_back_when_selected_meta_image_is_empty(self):
        product = Product.objects.create(
            name="Product With Empty Meta Creative",
            price="49.99",
            currency="USD",
            active=True,
            quantity=1,
            availability="in stock",
        )
        ProductImage.objects.create(
            product=product,
            image="products/images/storefront.jpg",
            thumbnail=True,
        )
        ProductImage.objects.create(product=product, image="", meta_image=True)

        response = self.client.get("/meta-catalog-feed.csv")
        rows = list(csv.DictReader(io.StringIO(response.content.decode("utf-8"))))
        product_row = next(row for row in rows if row["id"] == str(product.id))

        self.assertTrue(product_row["image_link"].endswith("/products/images/storefront.jpg"))

    def test_product_allows_only_one_meta_image(self):
        product = Product.objects.create(name="One Meta Image", price="10.00")
        ProductImage.objects.create(
            product=product,
            image="products/images/meta-one.jpg",
            meta_image=True,
        )
        duplicate = ProductImage(
            product=product,
            image="products/images/meta-two.jpg",
            meta_image=True,
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_admin_inline_can_replace_meta_image_in_one_submission(self):
        product = Product.objects.create(name="Replace Meta Image", price="10.00")
        replacement = ProductImage.objects.create(
            product=product,
            image="products/images/meta-two.jpg",
        )
        # Create the selected row second to prove saving does not rely on the
        # deselected row appearing first in the inline's primary-key order.
        current = ProductImage.objects.create(
            product=product,
            image="products/images/meta-one.jpg",
            meta_image=True,
        )
        formset_class = inlineformset_factory(
            Product,
            ProductImage,
            form=ProductImageInlineForm,
            formset=ProductImageInlineFormSet,
            fields=("image", "meta_image"),
            extra=0,
        )
        formset = formset_class(
            instance=product,
            data={
                "images-TOTAL_FORMS": "2",
                "images-INITIAL_FORMS": "2",
                "images-MIN_NUM_FORMS": "0",
                "images-MAX_NUM_FORMS": "1000",
                "images-0-id": str(replacement.id),
                "images-0-product": str(product.id),
                "images-0-image": replacement.image.name,
                "images-0-meta_image": "on",
                "images-1-id": str(current.id),
                "images-1-product": str(product.id),
                "images-1-image": current.image.name,
            },
        )

        self.assertTrue(formset.is_valid(), formset.errors)
        formset.save()
        current.refresh_from_db()
        replacement.refresh_from_db()
        self.assertFalse(current.meta_image)
        self.assertTrue(replacement.meta_image)

    def test_admin_inline_rejects_multiple_meta_images(self):
        product = Product.objects.create(name="Multiple Meta Images", price="10.00")
        first = ProductImage.objects.create(
            product=product,
            image="products/images/meta-one.jpg",
        )
        second = ProductImage.objects.create(
            product=product,
            image="products/images/meta-two.jpg",
        )
        formset_class = inlineformset_factory(
            Product,
            ProductImage,
            form=ProductImageInlineForm,
            formset=ProductImageInlineFormSet,
            fields=("image", "meta_image"),
            extra=0,
        )
        formset = formset_class(
            instance=product,
            data={
                "images-TOTAL_FORMS": "2",
                "images-INITIAL_FORMS": "2",
                "images-MIN_NUM_FORMS": "0",
                "images-MAX_NUM_FORMS": "1000",
                "images-0-id": str(first.id),
                "images-0-product": str(product.id),
                "images-0-image": first.image.name,
                "images-0-meta_image": "on",
                "images-1-id": str(second.id),
                "images-1-product": str(product.id),
                "images-1-image": second.image.name,
                "images-1-meta_image": "on",
            },
        )

        self.assertFalse(formset.is_valid())
        self.assertIn("meta_image", formset.forms[0].errors)
        self.assertIn("meta_image", formset.forms[1].errors)

    def test_meta_catalog_feed_includes_active_system_product_without_active_tiers(self):
        product = Product.objects.create(
            name="New System Without Ready Tiers",
            price="399.99",
            currency="USD",
            active=True,
            is_system=True,
            quantity=2,
            availability="in stock",
        )
        ProductVariant.objects.create(
            product=product,
            tier="basic",
            title="Draft Tier",
            price="399.99",
            currency="USD",
            active=False,
            quantity=2,
        )

        response = self.client.get("/meta-catalog-feed.csv")

        self.assertEqual(response.status_code, 200)
        csv_body = response.content.decode("utf-8")
        self.assertIn("New System Without Ready Tiers", csv_body)
        self.assertIn(str(product.id), csv_body)

    def test_meta_catalog_feed_ignores_malformed_image_values(self):
        product = Product.objects.create(
            name="Product With Bad Image Value",
            price="49.99",
            currency="USD",
            active=True,
            quantity=1,
            availability="in stock",
        )
        ProductImage.objects.create(product=product, image="", thumbnail=True)

        response = self.client.get("/meta-catalog-feed.csv")

        self.assertEqual(response.status_code, 200)
        csv_body = response.content.decode("utf-8")
        self.assertIn("Product With Bad Image Value", csv_body)


class SalePriceDisplayTests(TestCase):
    # Exercise the shared serializer and rendered price fragment so catalog and
    # detail pages cannot silently lose the original or sale amount again.
    def setUp(self):
        self.product = Product.objects.create(
            name="Sale display product", price="100.00", sale_price="80.00",
            active=True, quantity=3,
        )

    def test_simple_sale_is_available_to_catalog_and_detail(self):
        from decimal import Decimal
        from django.template.loader import render_to_string

        for tag in ("main", "single"):
            with self.subTest(tag=tag):
                data = self.product.serialize(tag)
                self.assertEqual(data["sale_price"], Decimal("80.00"))
                self.assertTrue(data["has_sale"])
                self.assertEqual(data["regular_price_display"], "$ 100.00")
                self.assertEqual(data["price_display"], "$ 80.00")
                html = render_to_string("shop/_sale_price.html", {"item": data})
                self.assertIn('<del class="product-price-original">$ 100.00</del>', html)
                self.assertIn('<span>$ 80.00</span>', html)

    def test_regular_price_has_no_strike_through(self):
        from django.template.loader import render_to_string

        self.product.sale_price = None
        data = self.product.serialize("single")
        self.assertFalse(data["has_sale"])
        html = render_to_string("shop/_sale_price.html", {"item": data})
        self.assertNotIn("<del", html)
        self.assertIn('<span>$ 100.00</span>', html)

    def test_normal_variant_ranges_use_active_options_not_parent_price(self):
        from .models import NormalProductVariant

        NormalProductVariant.objects.create(
            product=self.product, title="Sale option", price="30.00", sale_price="20.00",
        )
        NormalProductVariant.objects.create(
            product=self.product, title="Regular option", price="50.00",
        )
        NormalProductVariant.objects.create(
            product=self.product, title="Inactive option", price="200.00", active=False,
        )
        data = self.product.serialize("main")
        self.assertTrue(data["has_sale"])
        self.assertEqual(data["regular_price_display"], "$ 30.00 - $ 50.00")
        self.assertEqual(data["price_display"], "$ 20.00 - $ 50.00")
