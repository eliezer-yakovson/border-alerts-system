from fastapi import APIRouter
from dal import get_alerts_by_border_and_priority, get_distance_distribution, get_top_urgent_zones

router = APIRouter()

@router.get('/analytics/alerts-by-border-and-priority')
def alerts_by_border_and_priority():
    return get_alerts_by_border_and_priority()

@router.get('/analytics/top-urgent-zones')
def top_urgent_zones():
    return get_top_urgent_zones()

@router.get('/analytics/distance-distribution')
def distance_distribution():
    return get_distance_distribution()


