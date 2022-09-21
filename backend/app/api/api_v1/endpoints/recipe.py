# import asyncio
# from typing import Any, Optional

# import httpx
# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session

# from app import crud
# from app.api import deps
# from app.clients.reddit import RedditClient
# from app.schemas.recipe import (
#     Recipe,
#     RecipeCreate,
#     RecipeSearchResults,
#     RecipeUpdateRestricted,
# )
# from app.models.user import User

# router = APIRouter()
# RECIPE_SUBREDDITS = ["recipes", "easyrecipes", "TopSecretRecipes"]


# @router.get("/{recipe_id}", status_code=200, response_model=Recipe)
# async def fetch_recipe(
#     *,
#     recipe_id: int,
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     레시피를 조회합니다.
#     """
#     result = crud.recipe.get(db=db, id=recipe_id)
#     if not result:
#         # the exception is raised, not returned - you will get a validation
#         # error otherwise.
#         raise HTTPException(
#             status_code=404, detail=f"Recipe with ID {recipe_id} not found"
#         )

#     return result


# @router.get("/my-recipes/", status_code=200, response_model=RecipeSearchResults)
# async def fetch_user_recipes(
#     *,
#     db: Session = Depends(deps.get_db),
#     current_user: User = Depends(deps.get_current_user),
# ) -> Any:
#     """
#     로그인한 유저의 모든 레시피를 가져옵니다.
#     """
#     recipes = current_user.recipes
#     print(recipes)
#     if not recipes:
#         return {"results": list()}

#     return {"results": list(recipes)}


# @router.get("/search/", status_code=200, response_model=RecipeSearchResults)
# async def search_recipes(
#     *,
#     keyword: str = Query(None, min_length=3, example="chicken"),
#     max_results: Optional[int] = 10,
#     db: Session = Depends(deps.get_db),
# ) -> dict:
#     """
#     키워드 검색 결과에 따른 모든 레시피를 가져옵니다.
#     """
#     recipes = crud.recipe.get_multi(db=db, limit=max_results)
#     results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), recipes)

#     return {"results": list(results)}


# @router.post("/", status_code=201, response_model=Recipe)
# async def create_recipe(
#     *,
#     recipe_in: RecipeCreate,
#     db: Session = Depends(deps.get_db),
#     current_user: User = Depends(deps.get_current_user),
# ) -> dict:
#     """
#     새로운 레시피를 생성합니다.
#     """
#     if recipe_in.submitter_id != current_user.id:
#         raise HTTPException(
#             status_code=403, detail=f"You can only submit recipes as yourself"
#         )
#     recipe = crud.recipe.create(db=db, obj_in=recipe_in)

#     return recipe


# @router.put("/", status_code=200, response_model=Recipe)
# async def update_recipe(
#     *,
#     recipe_in: RecipeUpdateRestricted,
#     db: Session = Depends(deps.get_db),
#     current_user: User = Depends(deps.get_current_user),
# ) -> dict:
#     """
#     레시피를 업데이트합니다.
#     """
#     recipe = crud.recipe.get(db, id=recipe_in.id)
#     if not recipe:
#         raise HTTPException(
#             status_code=400, detail=f"Recipe with ID: {recipe_in.id} not found."
#         )

#     if recipe.submitter_id != current_user.id:
#         raise HTTPException(
#             status_code=403, detail=f"You can only update your recipes."
#         )

#     updated_recipe = crud.recipe.update(db=db, db_obj=recipe, obj_in=recipe_in)
#     return updated_recipe


# async def get_reddit_top_async(subreddit: str) -> list:
#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
#             headers={"User-agent": "recipe bot 0.1"},
#         )

#     subreddit_recipes = response.json()
#     subreddit_data = []
#     for entry in subreddit_recipes["data"]["children"]:
#         score = entry["data"]["score"]
#         title = entry["data"]["title"]
#         link = entry["data"]["url"]
#         subreddit_data.append(f"{str(score)}: {title} ({link})")
#     return subreddit_data


# @router.get("/ideas/async")
# async def fetch_ideas_async(
#     user: User = Depends(deps.get_current_active_superuser),
# ) -> dict:
#     results = await asyncio.gather(
#         *[get_reddit_top_async(subreddit=subreddit) for subreddit in RECIPE_SUBREDDITS]
#     )
#     return dict(zip(RECIPE_SUBREDDITS, results))


# @router.get("/ideas/")
# async def fetch_ideas(
#     reddit_client: RedditClient = Depends(deps.get_reddit_client),
# ) -> dict:
#     return {
#         key: reddit_client.get_reddit_top(subreddit=key) for key in RECIPE_SUBREDDITS
#     }
