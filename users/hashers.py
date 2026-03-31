from django.contrib.auth.hashers import BasePasswordHasher
from passlib.hash import phpass as wp_hash


class WordPressPasswordHasher(BasePasswordHasher):
    """
    Verify WordPress-style hashes stored in Django as:

        wordpress$P$...    or    wordpress$$P$...

    We rely on passlib's `phpass`, which is compatible with WordPress'
    $P$ hashes.
    """
    algorithm = "wordpress"

    def salt(self):
        # WordPress / PHPass hashes include their own salt.
        return None

    def encode(self, password, salt=None, iterations=None):
        """
        Not really needed for migration (we don't encode to WP), but
        Django requires this method. This produces: wordpress$<wp_hash>
        where <wp_hash> looks like $P$Bhhim...
        """
        raw = wp_hash.hash(password)  # e.g. "$P$Bhhim..."
        if not raw.startswith("$P$"):
            raise ValueError("Unexpected WP hash format from phpass: %r" % raw)
        return f"{self.algorithm}${raw}"

    def verify(self, password, encoded):
        try:
            algorithm, rest = encoded.split("$", 1)
        except ValueError:
            return False

        if algorithm != self.algorithm:
            return False

        # rest may be "$P$..." (your current DB) or "P$..." depending on import
        if rest.startswith("$P$"):
            wp_encoded = rest
        elif rest.startswith("P$"):
            wp_encoded = "$" + rest
        else:
            return False

        return wp_hash.verify(password, wp_encoded)

    def must_update(self, encoded):
        # After a successful login, rehash using Django's default hasher
        return True

    def safe_summary(self, encoded):
        try:
            algorithm, rest = encoded.split("$", 1)
        except ValueError:
            algorithm, rest = self.algorithm, ""
        return {
            "algorithm": algorithm,
            "hash": (rest[:10] + "...") if rest else "",
        }

    def harden_runtime(self, password, encoded):
        # no extra hardening
        pass
