def test_app():
    from summarize_bot.__init__ import create_app

    app = create_app()
    assert app
