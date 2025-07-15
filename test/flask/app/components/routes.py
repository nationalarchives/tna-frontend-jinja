import json

from app.components import bp
from flask import render_template, request


def render_component(template):
    params = request.args.get("params")
    return render_template(template, params=json.loads(params) if params else {})


@bp.route("/accordion")
def accordion():
    return render_component("widgets/accordion.html")


@bp.route("/breadcrumbs")
def breadcrumbs():
    return render_component("widgets/breadcrumbs.html")


@bp.route("/button")
def button():
    return render_component("widgets/button.html")


@bp.route("/card")
def card():
    return render_component("widgets/card.html")


@bp.route("/checkboxes")
def checkboxes():
    return render_component("widgets/checkboxes.html")


@bp.route("/compound-filters")
def compound_filters():
    return render_component("widgets/compound-filters.html")


@bp.route("/cookie-banner")
def cookie_banner():
    return render_component("widgets/cookie-banner.html")


@bp.route("/date-input")
def date_input():
    return render_component("widgets/date-input.html")


@bp.route("/date-search")
def date_search():
    return render_component("widgets/date-search.html")


@bp.route("/details")
def details():
    return render_component("widgets/details.html")


@bp.route("/error-summary")
def error_summary():
    return render_component("widgets/error-summary.html")


@bp.route("/file-input")
def file_input():
    return render_component("widgets/file-input.html")


@bp.route("/files-list")
def files_list():
    return render_component("widgets/files-list.html")


@bp.route("/footer")
def footer():
    return render_component("widgets/footer.html")


@bp.route("/gallery")
def gallery():
    return render_component("widgets/gallery.html")


@bp.route("/global-header")
def globalHeader():
    return render_component("widgets/global-header.html")


@bp.route("/header")
def header():
    return render_component("widgets/header.html")


@bp.route("/hero")
def hero():
    return render_component("widgets/hero.html")


@bp.route("/index-grid")
def index_grid():
    return render_component("widgets/index-grid.html")


@bp.route("/pagination")
def pagination():
    return render_component("widgets/pagination.html")


@bp.route("/phase-banner")
def phase_banner():
    return render_component("widgets/phase-banner.html")


@bp.route("/picture")
def picture():
    return render_component("widgets/picture.html")


@bp.route("/quick-filters")
def quick_filters():
    return render_component("widgets/quick-filters.html")


@bp.route("/radios")
def radios():
    return render_component("widgets/radios.html")


@bp.route("/search-field")
def search_field():
    return render_component("widgets/search-field.html")


@bp.route("/secondary-navigation")
def secondary_navigation():
    return render_component("widgets/secondary-navigation.html")


@bp.route("/select")
def select():
    return render_component("widgets/select.html")


@bp.route("/sidebar")
def sidebar():
    return render_component("widgets/sidebar.html")


@bp.route("/skip-link")
def skip_link():
    return render_component("widgets/skip-link.html")


@bp.route("/tabs")
def tabs():
    return render_component("widgets/tabs.html")


@bp.route("/text-input")
def text_input():
    return render_component("widgets/text-input.html")


@bp.route("/textarea")
def textarea():
    return render_component("widgets/textarea.html")


@bp.route("/warning")
def warning():
    return render_component("widgets/warning.html")
