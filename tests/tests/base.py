def test_import_settings(settings):
    assert "postgresql+asyncpg" in settings.APOSTGRES_URL, "Not loaded src path of project"
