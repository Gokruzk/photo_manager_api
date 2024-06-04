from fastapi import APIRouter, Path
from schema import ResponseSchema
from Routes.country import CountriesRoutes

router = APIRouter(
    prefix="/country",
    tags=["country"]
)


@router.get(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all():
    data = await CountriesRoutes.get_all()
    return ResponseSchema(detail="Successfully retreived", result=data)


@router.get(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_by_id(id: str = Path(..., alias="id")):
    data = await CountriesRoutes.get_by_id(int(id))
    return ResponseSchema(detail="Successfully retreived", result=data)
