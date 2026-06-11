from app import app


def _client():
    app.config["TESTING"] = True
    return app.test_client()


def test_index():
    res = _client().get("/")
    assert res.status_code == 200
    assert res.get_json()["service"] == "api-tickets"


def test_health():
    res = _client().get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_create_and_list_ticket():
    c = _client()
    res = c.post("/tickets", json={"title": "Imprimante en panne", "priority": "haute"})
    assert res.status_code == 201
    assert res.get_json()["title"] == "Imprimante en panne"

    res = c.get("/tickets")
    assert res.status_code == 200
    titles = [t["title"] for t in res.get_json()]
    assert "Imprimante en panne" in titles


def test_create_ticket_requires_title():
    res = _client().post("/tickets", json={"priority": "basse"})
    assert res.status_code == 400


def test_import_yaml():
    res = _client().post(
        "/tickets/import",
        data="- title: Souris cassee\n- title: Ecran noir\n  priority: haute\n",
        content_type="application/x-yaml",
    )
    assert res.status_code == 201
    assert res.get_json()["imported"] == 2
