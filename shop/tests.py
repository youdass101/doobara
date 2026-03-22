from django.test import TestCase

from .models import Product, ProductImage


class InternalProductFeedExportTests(TestCase):
    def setUp(self):
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
            ],
        )

        product_row = payload["products"][0]
        self.assertEqual(product_row["id"], str(self.product.id))
        self.assertEqual(product_row["title"], self.product.name)
        self.assertEqual(product_row["currency"], "USD")
        self.assertEqual(product_row["availability"], "in stock")
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
        self.assertIn("condition", product_row["missing_fields"])
