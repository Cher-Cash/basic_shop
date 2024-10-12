import pytest
from app import create_app, db
from models import Product


@pytest.fixture()
def testapp_fixture():
    test_app = create_app()
    test_app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Временная БД для тестов
        }
    )

    with test_app.app_context():
        db.create_all()  # Создаем таблицы
        # Добавьте тестовые данные, если необходимо
        sample_product = Product(name="Test Product")
        db.session.add(sample_product)
        db.session.commit()
    yield test_app


@pytest.fixture()
def client(testapp_fixture):
    return testapp_fixture.test_client()


@pytest.fixture()
def runner(testapp_fixture):
    return testapp_fixture.test_cli_runner()


def test_index_page(client):
    response = client.get("/")
    assert b"BUY" in response.data


def test_contact_page(client):
    response = client.get("/contact")
    assert b"kovach.aleksey19@ya.ru" in response.data
