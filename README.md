# Shuup Sandbox

## Copyright

Copyright (C) 2012-2019 by Shoop Commerce Ltd. <support@shuup.com>

Shuup is International Registered Trademark & Property of Shoop Commerce Ltd.,
Business ID: FI27184225,
Business Address: Iso-Roobertinkatu 20-22, 00120 HELSINKI, Finland.


## License

This source code is licensed under the SHUUP® ENTERPRISE EDITION -
END USER LICENSE AGREEMENT executed by Anders Innovations Inc. DBA as Shuup
and the Licensee.


## Steps to install this project:
1. Create folder for the application like /project
2. Under that create /var and /venv
3. Clone this repo under /project as app
   `git clone git@github.com:shuup/shuup-sandbox.git app`
4. Setup environment variables
5. Run requirements, migrate, init_multivendor_demo, collectstatic 
6. Runserver and you should be ready to go


## Notes:
1. If you get mysql error when running then you might want to install
   `mysqlclient==1.3.10`
2. If you are getting `OperationalError: no such table: main.shuup_contact__old`
   with sqlite, please consider downgrading your SQLite to 3.24.0.
   [To Github issue](https://github.com/shuup/shuup-project-template/issues/5).


## Development with this repository and Shuup

We recommend following directory structure when developing with Shuup.

```
project
    app (https://github.com/shuup/shuup-sandbox)
    var
    venv (project virtual environment if you are not using pyenv)
shuup-packages
    shuup (https://github.com/shuup/shuup)
    shuup-category-organizer (https://github.com/shuup/shuup-category-organizer)
    shuup-cms-blog (https://github.com/shuup/shuup-cms-blog)
    shuup-mailchimp (https://github.com/shuup/shuup-mailchimp)
    shuup-product-reviews (https://github.com/shuup/shuup-product-reviews)
    shuup-stripe (https://github.com/shuup/shuup-stripe)
    shuup-typography (https://github.com/shuup/shuup-typography)
    shuup-wishlist (https://github.com/shuup/shuup-wishlist)
    shuup-xtheme-extra-layouts (https://github.com/shuup/shuup-xtheme-extra-layouts)
    shuup-yaml (https://github.com/shuup/shuup-yaml)

    shuup-can-taxes (https://github.com/shuup/shuup-can-taxes)
    shuup-definite-theme (https://github.com/shuup/shuup-definite-theme)
    shuup-megastore-theme (https://github.com/shuup/shuup-megastore-theme)
    shuup-multivendor (https://github.com/shuup/shuup-multivendor)
    shuup-product-comparison (https://github.com/shuup/shuup-product-comparison)
    shuup-quickbooks (https://github.com/shuup/shuupp-quickbooks)
    shuup-stripe-connect (https://github.com/shuup/shuup-stripe-connect)
    shuup-stripe-subscriptions (https://github.com/shuup/shuup-stripe-subscriptions)
    shuup-subscriptions (https://github.com/shuup/shuup-subscriptions)
    shuup-us-taxes (https://github.com/shuup/shuup-us-taxes)
venv (general venv which contains all "shuup-packages" installed with
`pip install -e <package>`)
```

Point of this is that you likely want to install shuup-packages with
`pip instll -e <package>` which allows editing and speeds up the
development. This also applies to your own internal packages/addons you create.

We have included "business_logic" app to this project which you can use
for small business logic changes for your project.

See `update-dev-project.sh` for updating your local virtual environment for
this kind of setup. Pass path to your "shuup-packages"-directory and the
script should take care of the rest.

If you are not seeing styles after running the server. Make sure you have
run `python setup.py build_resources` for your "shuup-packages". This is
important when in development mode.


## Updating requirements

This project uses Prequ for requirements management.  To make changes to
installed packages or their versions, first install Prequ to the project
environment with::

  pip install prequ

To add/remove a requirement or update a requirement to a new version,
edit ``[prequ]`` section in ``setup.cfg`` and run::

  prequ update

This updates all ``requirements*.txt`` files and also builds new wheel
packages if needed.  Remember to commit any addition and removal of
files in the ``wheels`` directory too when committing the requirements
changes.
