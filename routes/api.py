from fastapi import APIRouter
from controller import suggestions_controller

router = APIRouter()
router.include_router(suggestions_controller.city_router)
