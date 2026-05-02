from fastapi import APIRouter, Depends
from dependencies import get_chart_service

router = APIRouter(prefix="/api/v1/charts", tags=["Charts"])

@router.get("/time-series/{room_id}")
async def get_time_series_chart(room_id: str, days: int = 7, chart_service=Depends(get_chart_service)):
    chart_data = chart_service.prepare_time_series_data(room_id, days)
    return chart_data

@router.get("/waste-comparison")
async def get_waste_comparison_chart(chart_service=Depends(get_chart_service)):
    chart_data = chart_service.prepare_waste_comparison_chart()
    return chart_data

@router.get("/device-breakdown")
async def get_device_breakdown_chart(room_id: str = None, chart_service=Depends(get_chart_service)):
    chart_data = chart_service.prepare_device_breakdown_chart(room_id)
    return chart_data

@router.get("/financial-trend")
async def get_financial_trend_chart(days: int = 30, chart_service=Depends(get_chart_service)):
    chart_data = chart_service.prepare_financial_trend_chart(days)
    return chart_data

@router.get("/occupancy-efficiency")
async def get_occupancy_efficiency_chart(chart_service=Depends(get_chart_service)):
    chart_data = chart_service.prepare_occupancy_efficiency_chart()
    return chart_data

@router.get("/dashboard")
async def get_dashboard_charts(chart_service=Depends(get_chart_service)):
    dashboard_data = chart_service.prepare_dashboard_summary()
    return dashboard_data
