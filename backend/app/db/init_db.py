import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
from app.core.config import settings
from app.enums.user_approve_status_flag import UserApproveStatusFlag

logger = logging.getLogger(__name__)


RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",  # noqa
    },
]

STORAGES = [
    {
        "name": "my_first_storage",
        "user_id": 1,
        "parent_id": None,
        "deleted_at": None,
    },
    {
        "name": "my_home",
        "user_id": 1,
        "parent_id": 1,
        "deleted_at": None,
    },
    {
        "name": "my_office",
        "user_id": 1,
        "parent_id": 1,
        "deleted_at": None,
    },
    {
        "name": "거실",
        "user_id": 1,
        "parent_id": 2,
        "deleted_at": None,
    },
    {
        "name": "침실",
        "user_id": 1,
        "parent_id": 2,
        "deleted_at": None,
    },
    {
        "name": "화장실",
        "user_id": 1,
        "parent_id": 2,
        "deleted_at": None,
    },
    {
        "name": "서랍장",
        "user_id": 1,
        "parent_id": 4,
        "deleted_at": None,
    },
    {
        "name": "벽장",
        "user_id": 1,
        "parent_id": 4,
        "deleted_at": None,
    },
    {
        "name": "옷장",
        "user_id": 1,
        "parent_id": 5,
        "deleted_at": None,
    }
]


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                name="Ford",
                password=settings.FIRST_SUPERUSER_PW,
                email=settings.FIRST_SUPERUSER,
                phone="010-0000-0000",
                level=10,
                point=100_000_000,
                business_class="business_class",
                business_name="business_name",
                business_president="ford",
                is_notification=True,
                approve_status_flag=UserApproveStatusFlag.A,
                is_superuser=True,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )
        if not user.recipes:
            for recipe in RECIPES:
                recipe_in = schemas.RecipeCreate(
                    label=recipe["label"],
                    source=recipe["source"],
                    url=recipe["url"],
                    submitter_id=user.id,
                )
                crud.recipe.create(db, obj_in=recipe_in)
        if not user.storages:
            for storage in STORAGES:
                storage_in = schemas.StorageCreate(
                    name=storage["name"],
                    user_id=storage["user_id"],
                    parent_id=storage["parent_id"],
                )
                crud.storage.create(db, obj_in=storage_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
