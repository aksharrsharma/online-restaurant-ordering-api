from fastapi.testclient import TestClient
from ..main import app
import pytest
from ..controllers import recipes as controller
from ..models import recipes as model

client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_recipe(db_session):
    recipe_data = {
        "title": " Carbonara",
        "ingredients": ["Spaghetti", "Eggs", "Pancetta", "Parmesan cheese"],
        "instructions": "Cook spaghetti for 5 minutes and strain. Mix eggs and cheese. Combine with pancetta."
    }

    recipe_object = model.Recipe(**recipe_data)

    created_recipe = controller.create(db_session, recipe_object)

# Assertions
    assert created_recipe is not None
    assert created_recipe.title == "Carbonara"
    assert created_recipe.ingredients ==  ["Spaghetti", "Eggs", "Pancetta", "Parmesan cheese"]
    assert created_recipe.instructions == "Cook spaghetti for 5 minutes and strain. Mix eggs and cheese. Combine with pancetta."
