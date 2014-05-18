HOT Imagery requests coordination service
=========================================

Development
===========

Virtual machine configuration
-----------------------------

* download and import VirtualBox Appliance (http://candela-it.com/hirc.ova)
  * ubuntu 14.04 with postgresql9.3 and postgis2.1
  * username:password `cit:cit`
  * forwarded ports
    * `ssh:2323`
    * `django:8000`
* personalize virtual machine environment, basically just copy your GitHub registered SSH key and git config file
  * `scp -P 2323 .ssh/id_rsa.pub cit@localhost:.ssh/id_rsa.pub`
  * `scp -P 2323 .ssh/id_rsa cit@localhost:.ssh/id_rsa`
  * `scp -P 2323 .gitconfig cit@localhost:.gitconfig`
* in `hirc` directory add your project fork remote: `git remote add origin git@github.com:your-git-username/hirc.git`
  * *upstream* repository is blessed (read-only) so you must add your (writable) *origin* remote


Simple development workflow
---------------------------

* fork blessed repository
* in forked repository work in local branches, keep your master clean, so you can sync it later with blessed repository: `git checkout -b mybranch`
* push your local branch changes: `git push origin mybranch:mybranch`
* create a pull request against the blessed repo
* same principles can be applied when working with other developers repositories:
  * `git remote add other_developer git@github.com:other_developer/hirc.git`
  * `git fetch other_developer`
  * `git checkout other_developer/his_branch`
  * ...


On the host(local) machine
--------------------------

* `mkdir /tmp/hirc_dev`
* `sshfs -p 2323 cit@localhost:hirc /tmp/hirc_dev/`
* open `/tmp/hirc_dev` in your favourite code editor


On the guest(virtual) machine
-----------------------------

* initialize Python virtual environment: `source ~/hirc_env/bin/activate`
* change directory `cd hirc` and run devserver: `hizashi.py devserver`
  * hizashi is a tiny wrapper around django https://github.com/dodobas/hizashi-utils
  * standard: `python manage.py runserver` also works
* open `http://localhost:8000` in your favourite web browser


Coding standards
----------------

* for better or worse we'll base it on: http://inasafe.org/en/developer-docs/coding_standards.html


Migrating database
------------------

* database migrations are somewhat fiddly in the beginning
  * `python manage.py migrate questions 0001`
  * `python manage.py migrate imagery_requests 0001`
  * `python manage.py migrate imagery_requests 0002`
  * `python manage.py migrate questions 0002`
