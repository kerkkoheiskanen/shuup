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
