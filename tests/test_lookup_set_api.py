from unittest.mock import Mock, patch


def _mock_response(status_code, json_data):
    resp = Mock()
    resp.status_code = status_code
    resp.json.return_value = json_data
    return resp


def test_lookup_set_success(client):
    set_response = _mock_response(200, {
        "name": "Tiny Plants",
        "theme_id": 5,
        "year": 2023,
        "num_parts": 758,
        "set_img_url": "https://example.com/img.jpg",
    })
    theme_response = _mock_response(200, {"name": "Botanicals"})

    with patch("main.requests.get", side_effect=[set_response, theme_response]):
        response = client.get("/lookup-set/10329")

    assert response.status_code == 200
    body = response.json()
    assert body["set_name"] == "Tiny Plants"
    assert body["theme"] == "Botanicals"
    assert body["year"] == 2023
    assert body["num_parts"] == 758


def test_lookup_set_not_found(client):
    with patch("main.requests.get", return_value=_mock_response(404, {})):
        response = client.get("/lookup-set/00000")

    assert response.status_code == 404


def test_lookup_set_falls_back_to_unknown_theme(client):
    set_response = _mock_response(200, {
        "name": "Mystery Set",
        "theme_id": 999,
        "year": 2024,
        "num_parts": 100,
        "set_img_url": None,
    })
    theme_response = _mock_response(500, {})

    with patch("main.requests.get", side_effect=[set_response, theme_response]):
        response = client.get("/lookup-set/12345")

    assert response.status_code == 200
    assert response.json()["theme"] == "Unknown"
