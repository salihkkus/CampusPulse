from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from datetime import datetime
import io
import csv
import numpy as np
from fpdf import FPDF
from dependencies import get_data_service, get_ai_engine, get_chart_service

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])

def tr(text):
    """Safe Turkish character mapping for PDF generation"""
    if not text: return ""
    maps = {
        'ş': 's', 'Ş': 'S', 'ı': 'i', 'İ': 'I', 'ğ': 'g', 'Ğ': 'G',
        'ç': 'c', 'Ç': 'C', 'ö': 'o', 'Ö': 'O', 'ü': 'u', 'Ü': 'U'
    }
    for k, v in maps.items():
        text = text.replace(k, v)
    return text

@router.get("/energy-audit")
async def get_energy_audit_report(data_service=Depends(get_data_service), ai_engine=Depends(get_ai_engine), chart_service=Depends(get_chart_service)):
    rooms_data = data_service.get_all_rooms_current_status()
    # ... (existing audit code)
    return {"status": "audit endpoint active"}

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Non-interactive backend

@router.get("/export/pdf")
async def export_report_pdf(
    startDate: str = Query(...),
    endDate: str = Query(...),
    startHour: int = 0,
    endHour: int = 23,
    data_service=Depends(get_data_service)
):
    report_data = data_service.get_range_analysis(startDate, endDate, startHour, endHour)
    if not report_data or "error" in report_data:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=400, content={"error": report_data.get("error", "Veri bulunamadi") if report_data else "Veri bulunamadi"})
    summary = report_data.get("summary", {})
    rooms = report_data.get("rooms", [])
    daily_stats = report_data.get("daily_stats", [])

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- SAYFA 1: KAPAK VE ÖZET ---
    pdf.add_page()
    
    # Header Design
    pdf.set_fill_color(16, 185, 129) # Emerald 500
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 24)
    pdf.set_xy(10, 10)
    pdf.cell(190, 20, tr("CampusPulse Enerji Analiz Raporu"), ln=True, align="L")
    
    pdf.set_font("Arial", "", 12)
    pdf.set_xy(10, 25)
    pdf.cell(190, 10, tr(f"Rapor Dönemi: {startDate} ile {endDate} arasi"), ln=True, align="L")
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(50)
    
    # Yönetici Özeti Kutusu
    pdf.set_fill_color(243, 244, 246)
    pdf.set_draw_color(209, 213, 219)
    pdf.rect(10, 50, 190, 50, 'DF')
    pdf.set_xy(15, 55)
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(180, 10, tr("Yönetici Özeti"), ln=True)
    
    pdf.set_text_color(55, 65, 81)
    pdf.set_font("Arial", "", 11)
    pdf.set_x(15)
    pdf.cell(90, 8, tr(f"Analiz Edilen Oda Sayisi: {summary.get('analyzed_rooms', 0)}"))
    pdf.cell(90, 8, tr(f"Toplam Enerji Tüketimi: {summary.get('total_power_kwh', 0):.1f} kWh"), ln=True)
    pdf.set_x(15)
    pdf.cell(90, 8, tr(f"Tahmini İsraf Maliyeti: {summary.get('total_waste_tl', 0):.2f} TL"))
    pdf.cell(90, 8, tr(f"Karbon Emisyonu: {summary.get('total_carbon_kg', 0):.1f} kg CO2"), ln=True)
    
    # --- GRAFİKLER (ALT ALTA) ---
    # 1. Enerji ve İsraf Trendi (Çift Eksen)
    pdf.set_y(110)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(190, 10, tr("1. Enerji ve İsraf Trendi"), ln=True)
    
    fig, ax1 = plt.subplots(figsize=(10, 4.5))
    dates = [d["date"][-5:] for d in daily_stats] # Sadece MM-DD
    tuketim = [d.get("total_power_kwh", 0) for d in daily_stats]
    israf = [d.get("total_waste_tl", 0) for d in daily_stats]
    
    if not daily_stats:
        # Boş veri durumu
        dates, tuketim, israf = ["Veri Yok"], [0], [0]

    ax1.set_xlabel(tr('Gün'))
    ax1.set_ylabel(tr('Tüketim (kWh)'), color='#10b981', fontsize=10, fontweight='bold')
    ax1.plot(dates, tuketim, marker='o', color='#10b981', label=tr('Tüketim (kWh)'), linewidth=2.5, markersize=8)
    ax1.tick_params(axis='y', labelcolor='#10b981')
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    ax2 = ax1.twinx()
    ax2.set_ylabel(tr('İsraf (TL)'), color='#f97316', fontsize=10, fontweight='bold')
    ax2.plot(dates, israf, marker='s', color='#f97316', linestyle='--', label=tr('İsraf (TL)'), linewidth=2)
    ax2.tick_params(axis='y', labelcolor='#f97316')
    
    plt.title(tr("Günlük Tüketim ve Kayıp Analizi"), fontsize=12, pad=15)
    fig.tight_layout()
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=150)
    img_buf.seek(0)
    img_buf.name = "chart1.png"
    pdf.image(img_buf, x=10, y=120, w=190)
    plt.close()
    
    # 2. En Yüksek İsraf Yapan Odalar
    pdf.set_y(205)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, tr("2. En Yüksek İsraf Yapan Odalar"), ln=True)
    
    plt.figure(figsize=(10, 4))
    waste_rooms = sorted(rooms, key=lambda x: x.get("total_waste_tl", 0), reverse=True)[:8]
    labels = [r["room_id"] for r in waste_rooms]
    costs = [r.get("total_waste_tl", 0) for r in waste_rooms]
    
    colors = plt.cm.Oranges(np.linspace(0.4, 0.8, len(labels)))
    plt.barh(labels[::-1], costs[::-1], color='#ef4444', alpha=0.8)
    plt.title(tr("En Yüksek Kayıp Yaşayan Odalar (TL)"), fontsize=11)
    plt.xlabel("TL")
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=150)
    img_buf.seek(0)
    img_buf.name = "chart2.png"
    pdf.image(img_buf, x=10, y=215, w=190)
    plt.close()

    # --- SAYFA 2: DAĞILIM VE TABLO ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, tr("3. Tüketim Dağılımı"), ln=True)
    pdf.ln(5)
    
    # Building Distribution Pie
    plt.figure(figsize=(5, 4))
    b_data = {}
    for r in rooms:
        b = r.get("building", "Diger")
        b_data[b] = b_data.get(b, 0) + r.get("total_power_kwh", 0)
    
    if b_data:
        plt.pie(b_data.values(), labels=b_data.keys(), autopct='%1.1f%%', 
                colors=['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899'],
                startangle=140, pctdistance=0.85)
        # draw circle
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title(tr("Bina Bazli Enerji Payi"), pad=10)
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=150)
    img_buf.seek(0)
    img_buf.name = "chart3.png"
    pdf.image(img_buf, x=10, y=30, w=90)
    plt.close()

    # Category Bar Chart
    plt.figure(figsize=(5, 4))
    c_data = {}
    for r in rooms:
        c = r["room_id"].split('_')[1] if '_' in r["room_id"] else "Oda"
        c_data[c] = c_data.get(c, 0) + r.get("total_power_kwh", 0)
    
    if c_data:
        plt.bar(list(c_data.keys()), list(c_data.values()), color='#8b5cf6', alpha=0.7)
        plt.title(tr("Kategori Bazli Tüketim (kWh)"), pad=10)
        plt.xticks(rotation=30, fontsize=8)
        plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=150)
    img_buf.seek(0)
    img_buf.name = "chart4.png"
    pdf.image(img_buf, x=105, y=30, w=90)
    plt.close()
    
    # 4. Detaylı Veri Tablosu
    pdf.set_y(100)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, tr("4. Detaylı Oda Analiz Listesi"), ln=True)
    pdf.ln(5)
    
    # Table Header
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(31, 41, 55) # Dark Gray
    pdf.set_text_color(255, 255, 255)
    pdf.cell(50, 10, tr("Oda ID"), 1, 0, 'C', True)
    pdf.cell(45, 10, tr("Tüketim (kWh)"), 1, 0, 'C', True)
    pdf.cell(45, 10, tr("Israf (TL)"), 1, 0, 'C', True)
    pdf.cell(50, 10, tr("Karbon (kg)"), 1, 1, 'C', True)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 9)
    for i, r in enumerate(rooms):
        fill = i % 2 == 1
        if fill: pdf.set_fill_color(243, 244, 246)
        else: pdf.set_fill_color(255, 255, 255)
        
        pdf.cell(50, 8, tr(r["room_id"]), 1, 0, 'L', True)
        pdf.cell(45, 8, f"{r.get('total_power_kwh', 0):.2f}", 1, 0, 'R', True)
        pdf.cell(45, 8, f"{r.get('total_waste_tl', 0):.2f}", 1, 0, 'R', True)
        pdf.cell(50, 8, f"{r.get('total_carbon_kg', 0):.2f}", 1, 1, 'R', True)

    pdf_output = pdf.output()
    return StreamingResponse(
        io.BytesIO(pdf_output),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=CampusPulse_Enerji_Raporu_{startDate}_{endDate}.pdf"}
    )

@router.get("/export/csv")
async def export_report_csv(
    startDate: str = Query(...),
    endDate: str = Query(...),
    startHour: int = 0,
    endHour: int = 23,
    data_service=Depends(get_data_service)
):
    report_data = data_service.get_range_analysis(startDate, endDate, startHour, endHour)
    rooms = report_data.get("rooms", [])
    summary = report_data.get("summary", {})

    output = io.StringIO()
    writer = csv.writer(output)
    
    # Rapor Bilgileri
    writer.writerow(["RAPOR BILGILERI"])
    writer.writerow(["Donem", f"{startDate} - {endDate}"])
    writer.writerow(["Oda Sayisi", summary.get("analyzed_rooms", 0)])
    writer.writerow(["Toplam Tuketim (kWh)", summary.get("total_power_kwh", 0)])
    writer.writerow(["Toplam Israf (TL)", summary.get("total_waste_tl", 0)])
    writer.writerow(["Toplam Karbon (kg)", summary.get("total_carbon_kg", 0)])
    writer.writerow([]) # Boş satır
    
    # Detaylı Veri
    writer.writerow(["ODA ANALIZ DETAYLARI"])
    writer.writerow(["Oda ID", "Bina", "Toplam Tuketim (kWh)", "Toplam Israf (TL)", "Toplam Karbon (kg)", "Ortalama Watt"])
    
    for r in rooms:
        writer.writerow([
            r["room_id"],
            r.get("building", "Diger"),
            round(r.get("total_power_kwh", 0), 2),
            round(r.get("total_waste_tl", 0), 2),
            round(r.get("total_carbon_kg", 0), 2),
            r.get("avg_power_watt", 0)
        ])

    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=CampusPulse_Veri_{startDate}_{endDate}.csv"}
    )
