import json

from flask import render_template, request

from app.components import bp


def render_component(template):
    params = request.args.get("params")
    context = json.loads(params) if params else {}
    return render_template(template, context=context)


@bp.route("/breadcrumbs")
def breadcrumbs():
    return render_component("breadcrumbs.html")


@bp.route("/button")
def button():
    return render_component("button.html")


@bp.route("/card")
def card():
    return render_component("card.html")


@bp.route("/cookie-banner")
def cookie_banner():
    return render_component("cookie-banner.html")


@bp.route("/filters")
def filters():
    return render_component("filters.html")


@bp.route("/footer")
def footer():
    return render_component("footer.html")


@bp.route("/grid")
def grid():
    return render_component("grid.html")


@bp.route("/header")
def header():
    return render_component("header.html")


@bp.route("/hero")
def hero():
    return render_component("hero.html")


@bp.route("/index-grid")
def index_grid():
    return render_component("index-grid.html")


@bp.route("/message")
def message():
    return render_component("message.html")


@bp.route("/phase-banner")
def phase_banner():
    return render_component("phase-banner.html")


@bp.route("/picture")
def picture():
    return render_component("picture.html")


@bp.route("/sensitive-image")
def sensitive_image():
    return render_component("sensitive-image.html")


@bp.route("/skip-link")
def skip_link():
    return render_component("skip-link.html")


@bp.route("/tabs")
def tabs():
    return render_component("tabs.html")
