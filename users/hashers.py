from django.contrib.auth.hashers import BasePasswordHasher
from passlib.hash import phpass as wp_hash  # <-- THIS is the right one


print("### users.hashers module imported ###")  # debug: should print once when Django starts


class WordPressPasswordHasher(BasePasswordHasher):
    """
    Verify WordPress-style hashes stored in Django as:

        wordpress$P$...    or    wordpress$$P$...

    We rely on passlib's `phpass`, which is compatible with WordPress'
    $P$ hashes.
    """
    print("### WordPressPasswordHasher class loaded ###")  # debug: should print once when Django starts
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
        # DEBUG: this should print when check_password() uses this hasher
        print(">>> WordPressPasswordHasher.verify CALLED")
        print("    password:", repr(password))
        print("    encoded:", repr(encoded))

        try:
            algorithm, rest = encoded.split("$", 1)
        except ValueError:
            print("    ! Could not split encoded string:", encoded)
            return False

        if algorithm != self.algorithm:
            print("    ! Algorithm mismatch:", algorithm)
            return False

        # rest may be "$P$..." (your current DB) or "P$..." depending on import
        if rest.startswith("$P$"):
            wp_encoded = rest
        elif rest.startswith("P$"):
            wp_encoded = "$" + rest
        else:
            print("    ! Not a valid WP hash segment:", rest)
            return False

        ok = wp_hash.verify(password, wp_encoded)
        print("    verify result:", ok)
        return ok

    def must_update(self, encoded):
        print(">>> WordPressPasswordHasher.must_update CALLED")
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
