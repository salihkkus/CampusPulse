import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import json

class DiagnosisEngine:
    """
    Enerji israfı teşhis motoru
    Anomali tespitinden sonra "neden" ve "ne yapmalı" sorularına cevap verir
    """
    
    def __init__(self):
        # Cihaz güç aralıkları (Watt)
        self.device_power_ranges = {
            "klima": {"min": 800, "max": 3500, "typical": 2000},
            "projeksiyon": {"min": 200, "max": 500, "typical": 300},
            "pc_20_adet": {"min": 2000, "max": 8000, "typical": 5000},
            "aydinlatma": {"min": 100, "max": 800, "typical": 400},
            "fiyans": {"min": 50, "max": 300, "typical": 150},
            "buzdolabi": {"min": 100, "max": 300, "typical": 200},
            "su_isitici": {"min": 1000, "max": 3000, "typical": 2000},
            "laboratuvar": {"min": 500, "max": 5000, "typical": 2000}
        }
        
        # Teşhis kuralları
        self.diagnosis_rules = self._initialize_diagnosis_rules()
        
        # Öneri şablonları
        self.recommendation_templates = self._initialize_recommendations()
        
    def _initialize_diagnosis_rules(self) -> Dict[str, Any]:
        """
        Teşhis kurallarını tanımla
        """
        return {
            # Boş oda + yüksek güç = israf
            "empty_room_high_power": {
                "condition": lambda data: data["occupancy_status"] == 0 and data["total_power"] > 500,
                "priority": "HIGH",
                "diagnosis_type": "waste"
            },
            
            # Ders var + anomali = arıza
            "class_session_anomaly": {
                "condition": lambda data: data["occupancy_status"] == 1 and data["is_anomaly"] == 1,
                "priority": "MEDIUM",
                "diagnosis_type": "fault"
            },
            
            # Ders dışı + klima açık
            "after_hours_ac": {
                "condition": lambda data: (
                    data["occupancy_status"] == 0 and 
                    data["hour_of_day"] not in [8, 9, 10, 11, 12, 13, 14, 15, 16, 17] and
                    self._detect_device("klima", data)
                ),
                "priority": "HIGH",
                "diagnosis_type": "waste"
            },
            
            # Hafta sonu + yüksek güç
            "weekend_waste": {
                "condition": lambda data: data["is_weekend"] == 1 and data["total_power"] > 200,
                "priority": "MEDIUM",
                "diagnosis_type": "waste"
            },
            
            # Tatil + güç var
            "holiday_waste": {
                "condition": lambda data: data["is_holiday"] == 1 and data["total_power"] > 100,
                "priority": "MEDIUM",
                "diagnosis_type": "waste"
            },
            
            # Gece + güç var
            "night_waste": {
                "condition": lambda data: (
                    data["hour_of_day"] in [22, 23, 0, 1, 2, 3, 4, 5, 6] and
                    data["total_power"] > 100
                ),
                "priority": "HIGH",
                "diagnosis_type": "waste"
            },
            
            # Ders saati + çok düşük güç
            "class_low_power": {
                "condition": lambda data: (
                    data["occupancy_status"] == 1 and 
                    data["total_power"] < 200 and
                    data["hour_of_day"] in [9, 10, 11, 14, 15, 16]
                ),
                "priority": "MEDIUM",
                "diagnosis_type": "fault"
            }
        }
    
    def _initialize_recommendations(self) -> Dict[str, Dict[str, str]]:
        """
        Öneri şablonlarını tanımla
        """
        return {
            "waste": {
                "klima": {
                    "short": "Klima açık unutulmuş",
                    "detailed": "Oda boş iken klima çalışıyor. Hemen kapatın.",
                    "action": "Klimayı kapat",
                    "savings": "Ayda ~{savings}TL tasarruf",
                    "priority": "HIGH"
                },
                "projeksiyon": {
                    "short": "Projeksiyon açık kalmış",
                    "detailed": "Oda boş iken projektör çalışıyor. Lambayı korumak için kapatın.",
                    "action": "Projeksiyonu kapat",
                    "savings": "Ayda ~{savings}TL tasarruf",
                    "priority": "MEDIUM"
                },
                "pc_20_adet": {
                    "short": "Bilgisayarlar açık kalmış",
                    "detailed": "Oda boş iken bilgisayarlar açık. Otomatik uyku modu ayarlayın.",
                    "action": "PC'leri kapat/uyku modu",
                    "savings": "Ayda ~{savings}TL tasarruf",
                    "priority": "HIGH"
                },
                "aydinlatma": {
                    "short": "Işıklar açık kalmış",
                    "detailed": "Oda boş iken ışıklar açık. Hareket sensörü takın.",
                    "action": "Işıkları kapat",
                    "savings": "Ayda ~{savings}TL tasarruf",
                    "priority": "MEDIUM"
                },
                "general": {
                    "short": "Cihazlar açık kalmış",
                    "detailed": "Oda boş iken cihazlar çalışıyor. Kontrol edip kapatın.",
                    "action": "Cihazları kontrol et",
                    "savings": "Ayda ~{savings}TL tasarruf",
                    "priority": "MEDIUM"
                }
            },
            "fault": {
                "power_failure": {
                    "short": "Güç arızası",
                    "detailed": "Ders varken güç tüketimi çok düşük. Elektrik arızası olabilir.",
                    "action": "Elektrik kontrolü",
                    "savings": "Ders kesintisi önlenir",
                    "priority": "HIGH"
                },
                "device_malfunction": {
                    "short": "Cihaz arızası",
                    "detailed": "Normal güce rağmen anomali tespit edildi. Cihaz arızası olabilir.",
                    "action": "Teknik servis çağır",
                    "savings": "Daha büyük arızalar önlenir",
                    "priority": "MEDIUM"
                },
                "sensor_error": {
                    "short": "Sensör hatası",
                    "detailed": "Veri okumalarında tutarsızlık var. Sensör kontrolü gerekli.",
                    "action": "Sensör kalibrasyonu",
                    "savings": "Doğru ölçüm",
                    "priority": "LOW"
                }
            }
        }
    
    def _detect_device(self, device_type: str, data: Dict[str, Any]) -> bool:
        """
        Güç tüketimine göre cihaz tespiti yap
        """
        if device_type not in self.device_power_ranges:
            return False
        
        # Cihazın güç aralığını kontrol et
        power_range = self.device_power_ranges[device_type]
        
        # Plug load watt'tan cihazı tespit et
        if device_type == "klima":
            return data["plug_load_watt"] >= power_range["min"]
        elif device_type == "projeksiyon":
            return data["projector_watt"] >= power_range["min"]
        elif device_type == "pc_20_adet":
            return data["plug_load_watt"] >= power_range["min"]
        elif device_type == "aydinlatma":
            return data["lighting_watt"] >= power_range["min"]
        else:
            return data["total_power"] >= power_range["min"]
    
    def _identify_wasting_devices(self, data: Dict[str, Any]) -> List[str]:
        """
        İsraf yapan cihazları tespit et
        """
        wasting_devices = []
        
        if data["occupancy_status"] == 0:  # Oda boşsa
            # Her cihazı kontrol et
            for device in self.device_power_ranges.keys():
                if self._detect_device(device, data):
                    wasting_devices.append(device)
        
        return wasting_devices
    
    def _calculate_potential_savings(self, data: Dict[str, Any], device_type: str) -> float:
        """
        Potansiyel tasarrufu hesapla (TL/ay)
        """
        # Elektrik fiyatı: 2.50 TL/kWh
        electricity_price = 2.50
        
        # Cihazın gücü
        if device_type == "klima":
            device_power = data["plug_load_watt"]
        elif device_type == "projeksiyon":
            device_power = data["projector_watt"]
        elif device_type == "pc_20_adet":
            device_power = data["plug_load_watt"]
        elif device_type == "aydinlatma":
            device_power = data["lighting_watt"]
        else:
            device_power = data["total_power"]
        
        # Aylık tahmini israf (günde 8 saat, 22 gün)
        monthly_waste_hours = 8 * 22
        monthly_waste_kwh = (device_power / 1000) * monthly_waste_hours
        monthly_cost = monthly_waste_kwh * electricity_price
        
        return monthly_cost
    
    def _get_device_priority(self, device_type: str, data: Dict[str, Any]) -> str:
        """
        Cihaz önceliğini belirle
        """
        # Güç tüketimine göre öncelik
        if device_type == "klima":
            return "HIGH"
        elif device_type == "pc_20_adet":
            return "HIGH"
        elif device_type == "projeksiyon":
            return "MEDIUM"
        elif device_type == "aydinlatma":
            return "MEDIUM"
        else:
            return "LOW"
    
    def diagnose_energy_waste(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enerji israfı teşhisi yap
        """
        diagnosis = {
            "room_id": data["room_id"],
            "timestamp": data.get("timestamp", datetime.now().isoformat()),
            "is_wasting": False,
            "diagnosis_type": None,
            "primary_issue": None,
            "detected_devices": [],
            "recommendations": [],
            "urgency_level": "LOW",
            "potential_savings": 0.0,
            "confidence": 0.0
        }
        
        # Tüm teşhis kurallarını kontrol et
        matched_rules = []
        
        for rule_name, rule_config in self.diagnosis_rules.items():
            try:
                if rule_config["condition"](data):
                    matched_rules.append({
                        "name": rule_name,
                        "priority": rule_config["priority"],
                        "type": rule_config["diagnosis_type"]
                    })
            except Exception as e:
                continue
        
        if not matched_rules:
            return diagnosis
        
        # En yüksek öncelikli kuralı seç
        primary_rule = max(matched_rules, key=lambda x: {
            "HIGH": 3, "MEDIUM": 2, "LOW": 1
        }.get(x["priority"], 0))
        
        diagnosis["is_wasting"] = True
        diagnosis["diagnosis_type"] = primary_rule["type"]
        diagnosis["urgency_level"] = primary_rule["priority"]
        diagnosis["confidence"] = 0.85  # Güven skoru
        
        # İsraf yapan cihazları tespit et
        if primary_rule["type"] == "waste":
            wasting_devices = self._identify_wasting_devices(data)
            diagnosis["detected_devices"] = wasting_devices
            
            # Her cihaz için öneri oluştur
            total_savings = 0.0
            
            for device in wasting_devices:
                savings = self._calculate_potential_savings(data, device)
                total_savings += savings
                
                # Öneri şablonunu al
                template = self.recommendation_templates.get("waste", {}).get(device, 
                    self.recommendation_templates["waste"]["general"])
                
                recommendation = {
                    "device": device,
                    "short": template["short"],
                    "detailed": template["detailed"],
                    "action": template["action"],
                    "savings": template["savings"].format(savings=f"{savings:.0f}"),
                    "priority": self._get_device_priority(device, data)
                }
                
                diagnosis["recommendations"].append(recommendation)
            
            diagnosis["potential_savings"] = total_savings
            
        elif primary_rule["type"] == "fault":
            # Arıza teşhisi
            fault_template = self.recommendation_templates["fault"]["device_malfunction"]
            
            diagnosis["recommendations"].append({
                "device": "system",
                "short": fault_template["short"],
                "detailed": fault_template["detailed"],
                "action": fault_template["action"],
                "savings": fault_template["savings"],
                "priority": fault_template["priority"]
            })
        
        # Ana sorunu belirle
        if diagnosis["recommendations"]:
            diagnosis["primary_issue"] = diagnosis["recommendations"][0]["short"]
        
        return diagnosis
    
    def generate_detailed_report(self, data: Dict[str, Any]) -> str:
        """
        Detaylı teşhis raporu oluştur
        """
        diagnosis = self.diagnose_energy_waste(data)
        
        if not diagnosis["is_wasting"]:
            return "✅ Her şey normal görünüyor. Herhangi bir israf tespit edilmedi."
        
        report = f"""
🔍 ENERJİ İSRAFI TEŞHİS RAPORU
========================

📍 Oda: {diagnosis['room_id']}
⏰ Zaman: {diagnosis['timestamp']}
🚨 Durum: {diagnosis['urgency_level']} öncelikli israf

🎯 Tespit Edilen Sorun: {diagnosis['primary_issue']}

🔧 Tespit Edilen Cihazlar: {', '.join(diagnosis['detected_devices'])}

💰 Potansiyel Tasarruf: {diagnosis['potential_savings']:.0f}TL/ay

📋 Öneriler:
"""
        
        for i, rec in enumerate(diagnosis['recommendations'], 1):
            report += f"""
{i}. {rec['short']}
   • Detay: {rec['detailed']}
   • Aksiyon: {rec['action']}
   • Tasarruf: {rec['savings']}
   • Öncelik: {rec['priority']}
"""
        
        report += f"""
📊 Güven Skoru: {diagnosis['confidence']:.0%}

⏱️ Hemen Müdahale Edilmeli!
"""
        
        return report
    
    def get_quick_diagnosis(self, data: Dict[str, Any]) -> str:
        """
        Hızlı teşhis (tek satır)
        """
        diagnosis = self.diagnose_energy_waste(data)
        
        if not diagnosis["is_wasting"]:
            return "✅ Normal"
        
        if diagnosis["detected_devices"]:
            devices_str = ", ".join(diagnosis["detected_devices"])
            return f"⚠️ {diagnosis['primary_issue']}: {devices_str}"
        else:
            return f"⚠️ {diagnosis['primary_issue']}"
    
    def batch_diagnose(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Toplu teşhis yap
        """
        results = []
        
        for data in data_list:
            diagnosis = self.diagnose_energy_waste(data)
            results.append(diagnosis)
        
        return results
    
    def get_diagnosis_summary(self, diagnoses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Teşhis özeti al
        """
        total = len(diagnoses)
        wasting = sum(1 for d in diagnoses if d["is_wasting"])
        
        device_counts = {}
        for diagnosis in diagnoses:
            for device in diagnosis["detected_devices"]:
                device_counts[device] = device_counts.get(device, 0) + 1
        
        urgency_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for diagnosis in diagnoses:
            if diagnosis["is_wasting"]:
                urgency_counts[diagnosis["urgency_level"]] += 1
        
        total_savings = sum(d["potential_savings"] for d in diagnoses)
        
        return {
            "total_analyzed": total,
            "wasting_count": wasting,
            "wasting_percentage": (wasting / total * 100) if total > 0 else 0,
            "device_frequency": device_counts,
            "urgency_distribution": urgency_counts,
            "total_potential_savings": total_savings,
            "avg_savings_per_waste": total_savings / wasting if wasting > 0 else 0
        }
