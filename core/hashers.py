from passlib.hash import ldap_salted_sha1
from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
from django.utils.translation import gettext_noop as _


class LDAPSaltedSHA1(BasePasswordHasher):
    algorithm = 'ldap_salted_sha1'

    def verify(self, password, encoded):
        encoded = encoded.replace('ldap_salted_sha1$', '{SSHA}')
        return ldap_salted_sha1.verify(password, encoded)

    def safe_summary(self, encoded):
        algorithm, current_hash = encoded.split('$', 2)

        return {
            _('algorithm'): algorithm,
            _('hash'): mask_hash(current_hash),
        }

    def encode(self, password, salt):
        encoded = ldap_salted_sha1.hash(password)
        return encoded.replace('{SSHA}', 'ldap_salted_sha1$')
