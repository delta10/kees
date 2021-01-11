# Security

This document describes the security aspects of the project.

## Authentication / authorisation

Authentication is done with username and password. Authorisation is handled inside the application. Administrators hand out user roles using the admin panel.

## Login procedure

The user logs in through the login page of the application. Two-factor authentication is not available in this application.

## Password policy

Password validation is provided by the Django framework. The minimum password length is 7 characters, see `AUTH_PASSWORD_VALIDATORS` in [settings.py](./kees/settings.py).

## Cryptography policy

Password hashes are stored using PBKDF2.  SSL / TLS encryption is handled on Kubernetes Ingress level. Encryption at rest can be handled by the storage provider in Kubernetes. See `PASSWORD_HASHERS` in [settings.py](./kees/settings.py).

## Backup policy

In production we will create a backup every four hours with a retention of 30 days.

