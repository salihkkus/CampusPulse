from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from datetime import datetime
import io
import csv
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
    summary = report_data.get("summary", {})
    rooms = report_data.get("rooms", [])

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- PAGE 1: COVER & EXECUTIVE SUMMARY ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(16, 185, 129) # Emerald 500
    pdf.cell(190, 30, tr("CampusPulse Enerji Analiz Raporu"), ln=True, align="C")
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, tr(f"Rapor Dönemi: {startDate} - {endDate}"), ln=True, align="C")
    pdf.ln(5)
    
    # Executive Summary Box
    pdf.set_fill_color(249, 250, 251)
    pdf.rect(10, 55, 190, 45, 'F')
    pdf.set_xy(15, 60)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(180, 10, tr("Yönetici Özeti"), ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(90, 7, tr(f"Analiz Edilen Oda Sayisi: {summary.get('analyzed_rooms', 0)}"))
    pdf.cell(90, 7, tr(f"Toplam Enerji Tüketimi: {summary.get('total_power_kwh', 0):.1f} kWh"), ln=True)
    pdf.cell(90, 7, tr(f"Toplam Israf Maliyeti: {summary.get('total_waste_tl', 0):.2f} TL"))
    pdf.cell(90, 7, tr(f"Karbon Ayak İzi: {summary.get('total_carbon_kg', 0):.1f} kg CO2"), ln=True)
    pdf.ln(10)

    # --- VERTICAL CHART STACKING ---
    # 1. Dual-Axis Energy & Waste Trend (Matching Image)
    pdf.set_font("Arial", "B", 13)
    pdf.set_y(105)
    pdf.cell(190, 10, tr("1. Enerji ve İsraf Trendi"), ln=True)
    
    fig, ax1 = plt.subplots(figsize=(10, 5))
    dates = [r["room_id"].split('_')[0] for r in rooms[:14]]
    tuketim = [r.get("total_power_kwh", 0) for r in rooms[:14]]
    israf = [r.get("total_waste_tl", 0) for r in rooms[:14]]
    
    # Left Axis: Tüketim
    ax1.set_xlabel(tr('Tarih'))
    ax1.set_ylabel(tr('Tüketim (kWh)'), color='#10b981')
    ax1.plot(dates, tuketim, marker='o', color='#10b981', label=tr('Tüketim'), linewidth=2)
    ax1.tick_params(axis='y', labelcolor='#10b981')
    
    # Right Axis: İsraf
    ax2 = ax1.twinx()
    ax2.set_ylabel(tr('İsraf (TL)'), color='#f97316')
    ax2.plot(dates, israf, marker='s', color='#f97316', linestyle='--', label=tr('İsraf'), linewidth=2)
    ax2.tick_params(axis='y', labelcolor='#f97316')
    
    plt.title(tr("Günlük Tüketim ve İsraf Trendi"))
    fig.tight_layout()
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=150)
    img_buf.seek(0)
    pdf.image(img_buf, x=10, y=115, w=190)
    plt.close()
    
    # 2. Top Waste Rooms (Horizontal Bars)
    pdf.set_y(210)
    pdf.cell(190, 10, tr("2. En Yüksek İsraf Yapan Odalar"), ln=True)
    
    plt.figure(figsize=(10, 4))
    waste_rooms = sorted(rooms, key=lambda x: x.get("total_waste_tl", 0), reverse=True)[:10]
    labels = [r["room_id"] for r in waste_rooms]
    costs = [r.get("total_waste_tl", 0) for r in waste_rooms]
    plt.barh(labels[::-1], costs[::-1], color='#ef4444')
    plt.title(tr("En Yüksek Kayıp Yaşayan İlk 10 Oda (TL)"))
    plt.tight_layout()
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=150)
    img_buf.seek(0)
    pdf.image(img_buf, x=10, y=220, w=190)
    plt.close()

    # --- PAGE 2: DISTRIBUTIONS & TABLE ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 13)
    pdf.cell(190, 10, tr("3. Tüketim Dağılım Analizleri"), ln=True)
    
    # Building Distribution Pie
    plt.figure(figsize=(6, 4))
    b_data = {}
    for r in rooms:
        b = r.get("building", "Diger")
        b_data[b] = b_data.get(b, 0) + r.get("total_power_kwh", 0)
    plt.pie(b_data.values(), labels=b_data.keys(), autopct='%1.1f%%', colors=['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6'])
    plt.title(tr("Bina Bazli Tüketim Payi"))
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=150)
    img_buf.seek(0)
    pdf.image(img_buf, x=10, y=30, w=90)
    plt.close()

    # Category Bar Chart
    plt.figure(figsize=(6, 4))
    c_data = {}
    for r in rooms:
        c = r["room_id"].split('_')[1] if '_' in r["room_id"] else "Diger"
        c_data[c] = c_data.get(c, 0) + r.get("total_power_kwh", 0)
    plt.bar(list(c_data.keys()), list(c_data.values()), color='#8b5cf6')
    plt.title(tr("Kategori Bazli Tüketim (kWh)"))
    plt.xticks(rotation=30)
    plt.tight_layout()
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=150)
    img_buf.seek(0)
    pdf.image(img_buf, x=105, y=30, w=90)
    plt.close()
    
    # 4. Detailed Data Table
    pdf.set_y(100)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(190, 10, tr("4. Detaylı Veri Tablosu"), ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 9)
    pdf.set_fill_color(229, 231, 235)
    pdf.cell(40, 8, tr("Oda ID"), 1, 0, 'C', True)
    pdf.cell(50, 8, tr("Tüketim (kWh)"), 1, 0, 'C', True)
    pdf.cell(50, 8, tr("İsraf (TL)"), 1, 0, 'C', True)
    pdf.cell(50, 8, tr("Emisyon (kg)"), 1, 1, 'C', True)
    
    pdf.set_font("Arial", "", 8)
    for i, r in enumerate(rooms):
        fill = i % 2 == 0
        if fill: pdf.set_fill_color(249, 250, 251)
        else: pdf.set_fill_color(255, 255, 255)
        
        pdf.cell(40, 7, tr(r["room_id"]), 1, 0, 'L', True)
        pdf.cell(50, 7, f"{r.get('total_power_kwh', 0):.2f}", 1, 0, 'R', True)
        pdf.cell(50, 7, f"{r.get('total_waste_tl', 0):.2f}", 1, 0, 'R', True)
        pdf.cell(50, 7, f"{r.get('total_carbon_kg', 0):.2f}", 1, 1, 'R', True)

    pdf_output = pdf.output()
    return StreamingResponse(
        io.BytesIO(pdf_output),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=CampusPulse_Rapor_{startDate}_{endDate}.pdf"}
    )

    pdf_output = pdf.output()
    return StreamingResponse(
        io.BytesIO(pdf_output),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=CampusPulse_Rapor_{startDate}_{endDate}.pdf"}
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

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Oda ID", "Bina", "Toplam Tüketim (kWh)", "Toplam Israf (TL)", "Toplam Karbon (kg)"])
    
    for r in rooms:
        writer.writerow([
            r["room_id"],
            r.get("building", "Diger"),
            round(r.get("total_power_kwh", 0), 2),
            round(r.get("total_waste_tl", 0), 2),
            round(r.get("total_carbon_kg", 0), 2)
        ])

    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=CampusPulse_Veri_{startDate}_{endDate}.csv"}
    )
