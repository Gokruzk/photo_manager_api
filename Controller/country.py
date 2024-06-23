from fastapi import APIRouter, Path, status
from schema import ResponseSchema
from Routes.country import CountriesRoutes

router = APIRouter(
    prefix="/country",
    tags=["country"]
)


@router.get(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all():
    try:
        data = await CountriesRoutes.get_all()
    except Exception as e:
        print(e)
        return ResponseSchema(status_code=status.HTTP_400_BAD_REQUEST, detail="Error retreiving data")
    else:
        return ResponseSchema(status_code=status.HTTP_200_OK, detail="Successfully retreived", result=data)


@router.get(path="/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_by_id(id: str = Path(..., alias="id")):
    try:
        data = await CountriesRoutes.get_by_id(int(id))
        ld = dict(data)
        if "cod_ubi" not in ld:
            raise Exception
    except Exception as e:
        print(e)
        return ResponseSchema(status_code=status.HTTP_400_BAD_REQUEST, detail="The country does not exist")
    else:
        return ResponseSchema(status_code=status.HTTP_200_OK, detail="Successfully retreived", result=data)
