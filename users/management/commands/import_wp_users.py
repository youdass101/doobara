import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = "Import users from WordPress CSV export"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to wp_users.csv")

    @transaction.atomic
    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"])

        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {csv_path}"))
            return

        created = 0
        skipped = 0

        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get("user_email", "").strip()
                username = row.get("user_login", "").strip()
                display_name = row.get("display_name", "").strip()
                wp_id = row.get("ID")
                wp_pass = row.get("user_pass", "").strip()


                if not email:
                    skipped += 1
                    continue

                # avoid duplicates if you run twice
                if User.objects.filter(email=email).exists():
                    skipped += 1
                    continue

                if not username:
                    username = email.split("@")[0]

                user = User(
                    username=username,
                    email=email,
                    id=wp_id,
                )

                # store WP hash in Django format: algorithm$hash
                user.password = f"wordpress${wp_pass}"

                # you can add extra fields if your custom User model has them:
                # user.first_name = row.get("billing_first_name", "") or ""
                # user.last_name = row.get("billing_last_name", "") or ""

                # set unusable password -> user must reset password
                user.save()

                # Optional: store old wp_id somewhere for later mapping
                # If you have a profile model or custom field, add it:
                # user.wp_id = wp_id
                # user.save()

                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import finished. Created: {created}, Skipped: {skipped}"
            )
        )
