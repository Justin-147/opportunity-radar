from opportunity_radar.writers.html_writer import render_html


def test_html_title_is_escaped():
    html = render_html("# Report", 'Bad <script>alert(1)</script>', "en")

    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_html_language_is_limited():
    html = render_html("# Report", "Title", '"><script>')

    assert '<html lang="en">' in html
