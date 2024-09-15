from fastapi import APIRouter, Path, status, Response
from routes.country import CountriesRoutes
from schema import ResponseSchema

router = APIRouter(
    prefix="/country",
    tags=["country"]
)


@router.get(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all():
    try:
        # get countries
        data = await CountriesRoutes.get_all()
        if data is False:
            raise Exception
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error retreiving data").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")
