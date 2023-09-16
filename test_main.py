from flask.testing import FlaskClient

# from urlshort import create_app


def test_shorten(client: FlaskClient):
    response = client.get("/")
    assert "Shorten" in response.text
