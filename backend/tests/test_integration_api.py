"""
Integration tests exercising the full FastAPI app via TestClient, covering
the mandatory demo flow end to end: shorten -> redirect -> analytics, plus
negative/error paths that a happy-path-only AI draft would likely miss.
"""


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_full_shorten_redirect_analytics_flow(client):
    shorten_resp = client.post(
        "/shorten", json={"original_url": "https://example.com/some/page"}
    )
    assert shorten_resp.status_code == 201
    body = shorten_resp.json()
    short_code = body["short_code"]
    assert body["original_url"] == "https://example.com/some/page"
    assert short_code in body["short_url"]

    redirect_resp = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_resp.status_code == 307
    assert redirect_resp.headers["location"] == "https://example.com/some/page"

    analytics_resp = client.get(f"/analytics/{short_code}")
    assert analytics_resp.status_code == 200
    analytics = analytics_resp.json()
    assert analytics["click_count"] == 1
    assert analytics["last_clicked_at"] is not None


def test_shorten_with_custom_alias(client):
    resp = client.post(
        "/shorten",
        json={"original_url": "https://example.com", "custom_alias": "myLink1"},
    )
    assert resp.status_code == 201
    assert resp.json()["short_code"] == "myLink1"


def test_shorten_duplicate_custom_alias_returns_409(client):
    client.post("/shorten", json={"original_url": "https://a.com", "custom_alias": "dupe123"})
    resp = client.post("/shorten", json={"original_url": "https://b.com", "custom_alias": "dupe123"})
    assert resp.status_code == 409


def test_shorten_rejects_invalid_url_scheme(client):
    resp = client.post("/shorten", json={"original_url": "ftp://example.com/file"})
    assert resp.status_code == 422


def test_shorten_rejects_empty_url(client):
    resp = client.post("/shorten", json={"original_url": ""})
    assert resp.status_code == 422


def test_redirect_unknown_short_code_returns_404(client):
    resp = client.get("/doesNotExist", follow_redirects=False)
    assert resp.status_code == 404


def test_analytics_unknown_short_code_returns_404(client):
    resp = client.get("/analytics/doesNotExist")
    assert resp.status_code == 404


def test_multiple_clicks_increment_analytics_correctly(client):
    shorten_resp = client.post("/shorten", json={"original_url": "https://example.com"})
    short_code = shorten_resp.json()["short_code"]

    for _ in range(3):
        client.get(f"/{short_code}", follow_redirects=False)

    analytics = client.get(f"/analytics/{short_code}").json()
    assert analytics["click_count"] == 3


def test_copilot_analyze_url_shortener_requirement(client):
    resp = client.post(
        "/copilot/analyze",
        json={
            "requirement": "Build a scalable URL shortener service with APIs, persistence, and analytics."
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["requirement_analysis"]["functional_requirements"]) >= 5
    assert len(body["task_decomposition"]) >= 5
    assert len(body["risk_analysis"]["risks"]) >= 3


def test_copilot_analyze_rejects_too_short_requirement(client):
    resp = client.post("/copilot/analyze", json={"requirement": "short"})
    assert resp.status_code == 422
