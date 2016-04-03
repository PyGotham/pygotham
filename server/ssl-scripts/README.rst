===================================
Generate and Renew SSL Certificates
===================================

SSL certificates are created using ``letsencrypt``. To renew the certificates,
run::

    $ pip install --user --upgrade letsencrypt
    $ ./generate-certificates.sh

Creating certificates uses the same ``letsencrypt`` command, just without the
``renew`` option. This is a manual step that only needs to be done once. Future
iterations of this setup should be handled via ansible.

.. note::

    This script must be run with sufficient priveleges. Typically, this means
    running as root or with ``sudo``.
