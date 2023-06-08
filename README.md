# The National Archives Frontend Jinja2 Templates

Jinja2 implementation of [TNA components](https://github.com/nationalarchives/tna-frontend) for inclusion in Python applications.

The rationale behind choosing Jinja was that it works with the two most popular Python frameworks:

- Django - [Django has support for the Jinja2 template engine](https://docs.djangoproject.com/en/4.2/topics/templates/#support-for-template-engines) which is then extended to [Wagtail support for Jinja](https://docs.wagtail.org/en/stable/reference/jinja2.html)
- Flask - [Jinja2 is the default template engine for Flask](https://flask.palletsprojects.com/en/2.3.x/templating/)

## Output

The Jinja2 templates and macros will be published to [PyPi](https://pypi.org/) which can then be included as a dependecy in Python projects.

For a full relationship diagram, see https://github.com/nationalarchives/tna-frontend#component-diagram.
