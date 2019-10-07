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
1. Create folder for the application like `/project`
2. Under that create `/var` and `/venv`
3. Clone this repo under `/project` as `app`
  ```bash
  $ git clone git@github.com:shuup/shuup-sandbox.git app
  ```
4. Setup environment variables
5. Run `requirements`, `migrate`, `init_multivendor_demo`, `collectstatic`
6. `Runserver` and you should be ready to go


## Notes:
1. If you get mysql error when running then you might want to install `mysqlclient==1.3.10`
2. If you are getting `OperationalError: no such table: main.shuup_contact__old` with `sqlite`, please consider downgrading your SQLite to 3.24.0 ( [to Github issue](https://github.com/shuup/shuup-project-template/issues/5) ).


## Development with this repository and Shuup

We recommend the following directory structure when developing with Shuup.

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
venv (general venv which contains all "shuup-packages" installed with `pip install -e <package>`)
```

Point of this is that you likely want to install shuup-packages with `$ pip install -e <package>` which allows editing and speeds up the development. This also applies to your own internal packages/addons you create.

We have included `business_logic` app to this project which you can use for small business logic changes for your project.

See `update-dev-project.sh` for updating your local virtual environment for this kind of setup. Pass path to your `shuup-packages` directory and the script should take care of the rest.

If you are not seeing styles after running the server. Make sure you have run `$ python setup.py build_resources` for your `shuup-packages`. This is important when in development mode.


## Development with this repository and Shuup with Docker

1. Create a local `shuup-packages` folder on the same level with the directory you keep the `shuup-sandbox` project files in. If you decide to install your packages somewhere else, you should open the `docker-compose.yml` file and edit the `../shuup-packages/` (under the `services -> django -> volumes`) path to point to your packages directory.

2. Place the main Shuup repository and all the Shuup Addons repositories you need in the `shuup-packages` folder. You can manually copy the required files and packages, but generally it's best to use the `git clone` command (`$ git clone git@github.com:shuup/shuup.git`, etc).

3. Run `$ docker-compose up --build`.

4. Run `$ docker exec -it sandbox bash`

    4.1. Run `$ bash update-dev-project.sh shuup-packages` inside the container to install required packages from `requirements.txt` file and local `shuup-packages` directory.

    4.2. Run `$ bash build_resources.sh shuup-packages` inside the container to build resources for Shuup addons.

5. Setup environment variables if needed. Copy the content of the `.env.template-docker` file to a new `.env` file and edit it if necessary (for example by choosing MySQL over PostgreSQL database on the `DATABASE_URL` line).

6. Django stuff

    6.1. Run `$ python manage.py migrate` to prime the database.

    6.2. Run `$ python manage.py init_multivendor_demo` to initialize the multivendor demo, if needed.

    6.3. Run `$ python manage.py collectstatic` to collect all static files to `/var/static/`, if needed.

    6.4. Run `$ python manage.py runserver 0.0.0.0:8000` to start the server.

7. Done.


## Updating requirements

This project uses [Prequ](https://pypi.org/project/prequ/) for requirements management.  To make changes to installed packages or their versions, first install Prequ to the project environment with:
```bash
$ pip install prequ
```
To add/remove a requirement or update a requirement to a new version, edit `[prequ]` section in `setup.cfg` and run::
```bash
$ prequ update
```
This updates all `requirements*.txt` files and also builds new wheel
packages if needed.  Remember to commit any addition and removal of
files in the `wheels` directory too when committing the requirements
changes.
