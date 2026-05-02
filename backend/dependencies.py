from data_service import DataService
from ai_engine import AIEngine
from frontend_bridge import FrontendBridge
from chart_data_service import ChartDataService
from enhanced_ai_engine import EnhancedAIEngine

# Global Instances (Singletons)
data_service = DataService()
ai_engine = AIEngine()
frontend_bridge = FrontendBridge()
chart_service = ChartDataService(data_service=data_service, ai_engine=ai_engine)
enhanced_ai = EnhancedAIEngine()

def get_data_service():
    return data_service

def get_ai_engine():
    return ai_engine

def get_enhanced_ai():
    return enhanced_ai

def get_frontend_bridge():
    return frontend_bridge

def get_chart_service():
    return chart_service
