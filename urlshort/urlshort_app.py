import json, os
from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    url_for,
    request,
    session,
)
from werkzeug.utils import secure_filename
from pathlib import Path

bp = Blueprint(name="urlshort", import_name=__name__)


@bp.route("/")
def home():
    return render_template("home.html", codes=session.keys())


@bp.route("/your-url", methods=["GET", "POST"])
def shorten_url():
    if request.method == "POST":
        code = request.form.get("code")
        urls: dict = {}

        # check if file already exisst
        if os.path.exists("urls.json"):
            with open("urls.json") as urls_file:
                urls = json.load(urls_file)

        # check if provided code already exists as key in the urls json file
        if code in urls:
            flash(
                "That short name has already been taken. Please select a different one."
            )
            return redirect(url_for("urlshort.home"))

        if "url" in request.form:
            urls[code] = {"url": request.form.get("url")}
        else:
            file_upload = request.files.get("file")
            filename = f"{code}-{secure_filename(file_upload.filename)}"
            file_upload.save(
                Path(
                    f"D:/projects/flaskapps/url-shotener/urlshort/static/user_fileuploads/{filename}"
                )
            )
            urls[code] = {"file": filename}

        with open("urls.json", "w+") as url_file:
            json.dump(urls, url_file)
            session[code] = True

        return render_template("your_url.html", code=code)

    return redirect(url_for("urlshort.home"))


@bp.route("/<string:code>")
def redirect_to_url(code: str):
    if os.path.exists("urls.json"):
        with open("urls.json") as urls_file:
            urls = json.load(urls_file)
            if code in urls:
                if "url" in urls.get(code):
                    return redirect(location=urls.get(code).get("url"))
                return redirect(
                    url_for(
                        "static",
                        filename=f"user_fileuploads/{urls.get(code).get('file')}",
                    )
                )
    return abort(404)


@bp.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html", error=error)


@bp.route("/api")
def session_api():
    return jsonify(list(session.keys()))
