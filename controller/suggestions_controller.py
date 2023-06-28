from fastapi import APIRouter
from service.suggestions_service import GetCity

city_router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@city_router.get("/suggestions")
async def get_suggestions(q: str, latitude: float, longitude: float, ):
    data_dict = {
        "city": q,
        "lat": latitude,
        "long": longitude
    }
    get_suggest_city_name = GetCity.get_suggest_city(data_dict)
    return get_suggest_city_name
