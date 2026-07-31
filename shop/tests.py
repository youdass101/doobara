import csv
import io

from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.test import TestCase, override_settings

from .admin import ProductImageInlineForm, ProductImageInlineFormSet
from .modeling.serialize_helper import product_serialize
from .models import Categorie, Product, ProductImage, ProductVariant


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
    def test_meta_catalog_feed_is_not_cached(self):
        response = self.client.get("/meta-catalog-feed.csv")

        self.assertIn("no-cache", response.headers["Cache-Control"])
        self.assertIn("no-store", response.headers["Cache-Control"])

    def test_meta_image_is_excluded_from_storefront_images(self):
        product = Product.objects.create(name="Separate Meta Creative", price="10.00")
        storefront = ProductImage.objects.create(
            product=product,
            image="products/images/storefront.jpg",
            thumbnail=True,
        )
        ProductImage.objects.create(
            product=product,
            image="products/images/meta-only.jpg",
            meta_image=True,
        )

        serialized = product_serialize(product, "product")

        self.assertEqual(serialized["main_image"]["url"], storefront.image.url)
        self.assertEqual(
            [image["url"] for image in serialized["all_images"]],
            [storefront.image.url],
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
