from django.test import TestCase

from .models import Categorie, Product, ProductImage


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
