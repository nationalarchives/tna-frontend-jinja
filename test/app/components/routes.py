import json
from app.components import bp

from flask import render_template, request


def render_component(template):
    params = request.args.get("params")
    context = json.loads(params) if params else {}
    return render_template(template, context=context)


@bp.route("/accordion")
def accordion():
    return render_component("accordion.html")


@bp.route("/breadcrumbs")
def breadcrumbs():
    return render_component("breadcrumbs.html")


@bp.route("/button")
def button():
    return render_component("button.html")


@bp.route("/card")
def card():
    return render_component("card.html")


@bp.route("/checkboxes")
def checkboxes():
    return render_component("checkboxes.html")


@bp.route("/compound-filters")
def compound_filters():
    return render_component("compound-filters.html")


@bp.route("/cookie-banner")
def cookie_banner():
    return render_component("cookie-banner.html")


@bp.route("/date-input")
def date_input():
    return render_component("date-input.html")


@bp.route("/date-search")
def date_search():
    return render_component("date-search.html")


@bp.route("/details")
def details():
    return render_component("details.html")


@bp.route("/error-summary")
def error_summary():
    return render_component("error-summary.html")


@bp.route("/files-list")
def files_list():
    return render_component("files-list.html")


@bp.route("/footer")
def footer():
    return render_component("footer.html")


@bp.route("/gallery")
def gallery():
    return render_component("gallery.html")


@bp.route("/global-header")
def globalHeader():
    return render_component("global-header.html")


@bp.route("/header")
def header():
    return render_component("header.html")


@bp.route("/hero")
def hero():
    return render_component("hero.html")


@bp.route("/index-grid")
def index_grid():
    return render_component("index-grid.html")


@bp.route("/pagination")
def pagination():
    return render_component("pagination.html")


@bp.route("/phase-banner")
def phase_banner():
    return render_component("phase-banner.html")


@bp.route("/picture")
def picture():
    return render_component("picture.html")


@bp.route("/quick-filters")
def quick_filters():
    return render_component("quick-filters.html")


@bp.route("/radios")
def radios():
    return render_component("radios.html")


@bp.route("/search-field")
def search_field():
    return render_component("search-field.html")


@bp.route("/secondary-navigation")
def secondary_navigation():
    return render_component("secondary-navigation.html")


@bp.route("/select")
def select():
    return render_component("select.html")


@bp.route("/sidebar")
def sidebar():
    return render_component("sidebar.html")


@bp.route("/skip-link")
def skip_link():
    return render_component("skip-link.html")


@bp.route("/tabs")
def tabs():
    return render_component("tabs.html")


@bp.route("/text-input")
def text_input():
    return render_component("text-input.html")


@bp.route("/textarea")
def textarea():
    return render_component("textarea.html")


@bp.route("/warning")
def warning():
    return render_component("warning.html")
