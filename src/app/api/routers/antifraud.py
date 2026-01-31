from fastapi import APIRouter, Depends
import hashlib, json

from ...api.schemas import AntifraudRequest, AntifraudResponse
from ...services import AntifraudService
from ...dependencies.cache import get_cache

router = APIRouter(prefix="/antifraud", tags=["antifraud"])

def generate_cache_key(request: AntifraudRequest) -> str:
    request_dict = request.model_dump(mode="json")
    sorted_json = json.dumps(request_dict, sort_keys=True)
    return f"antifraud_hash: {hashlib.md5(sorted_json.encode()).hexdigest()}"

@router.post("/check", response_model=AntifraudResponse)
def check_antifraud(request: AntifraudRequest, cache=Depends(get_cache)) -> AntifraudResponse:
    request_dict = request.model_dump()
    key = generate_cache_key(request)

    cached = cache.get(key)
    if cached:
        return AntifraudResponse.model_validate_json(cached)

    stop_factors = AntifraudService.check(request)
    
    response = AntifraudResponse(
        stop_factors=[sf.value for sf in stop_factors],
        result=len(stop_factors) == 0
    )

    cache.set(key, response.model_dump_json())
    return response