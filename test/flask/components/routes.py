import json
from test.flask.components import bp

from flask import render_template, request


def render_component(template):
    params = request.args.get("params")
    return render_template(template, params=json.loads(params) if params else {})


@bp.route("/accordion")
def accordion():
    return render_component("components/accordion.html")


@bp.route("/breadcrumbs")
def breadcrumbs():
    return render_component("components/breadcrumbs.html")


@bp.route("/button")
def button():
    return render_component("components/button.html")


@bp.route("/card")
def card():
    return render_component("components/card.html")


@bp.route("/checkboxes")
def checkboxes():
    return render_component("components/checkboxes.html")


@bp.route("/compound-filters")
def compound_filters():
    return render_component("components/compound-filters.html")


@bp.route("/cookie-banner")
def cookie_banner():
    return render_component("components/cookie-banner.html")


@bp.route("/date-input")
def date_input():
    return render_component("components/date-input.html")


@bp.route("/date-search")
def date_search():
    return render_component("components/date-search.html")


@bp.route("/details")
def details():
    return render_component("components/details.html")


@bp.route("/error-summary")
def error_summary():
    return render_component("components/error-summary.html")


@bp.route("/files-list")
def files_list():
    return render_component("components/files-list.html")


@bp.route("/footer")
def footer():
    return render_component("components/footer.html")


@bp.route("/gallery")
def gallery():
    return render_component("components/gallery.html")


@bp.route("/global-header")
def globalHeader():
    return render_component("components/global-header.html")


@bp.route("/header")
def header():
    return render_component("components/header.html")


@bp.route("/hero")
def hero():
    return render_component("components/hero.html")


@bp.route("/index-grid")
def index_grid():
    return render_component("components/index-grid.html")


@bp.route("/pagination")
def pagination():
    return render_component("components/pagination.html")


@bp.route("/phase-banner")
def phase_banner():
    return render_component("components/phase-banner.html")


@bp.route("/picture")
def picture():
    return render_component("components/picture.html")


@bp.route("/quick-filters")
def quick_filters():
    return render_component("components/quick-filters.html")


@bp.route("/radios")
def radios():
    return render_component("components/radios.html")


@bp.route("/search-field")
def search_field():
    return render_component("components/search-field.html")


@bp.route("/secondary-navigation")
def secondary_navigation():
    return render_component("components/secondary-navigation.html")


@bp.route("/select")
def select():
    return render_component("components/select.html")


@bp.route("/sidebar")
def sidebar():
    return render_component("components/sidebar.html")


@bp.route("/skip-link")
def skip_link():
    return render_component("components/skip-link.html")


@bp.route("/tabs")
def tabs():
    return render_component("components/tabs.html")


@bp.route("/text-input")
def text_input():
    return render_component("components/text-input.html")


@bp.route("/textarea")
def textarea():
    return render_component("components/textarea.html")


@bp.route("/warning")
def warning():
    return render_component("components/warning.html")
