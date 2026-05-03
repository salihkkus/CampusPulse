import React, { Suspense } from 'react';
import { Link } from 'react-router-dom';
import ThreeDMap from '../components/ThreeDMap';

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#fcf8ff] text-[#1b1b23] font-body-md">
      {/* TopNavBar */}
      <nav className="fixed top-0 w-full z-50 bg-white/70 backdrop-blur-xl border-b border-white/20 shadow-sm transition-all duration-300">
        <div className="flex justify-between items-center px-6 py-4 max-w-7xl mx-auto">
          <Link to="/" className="text-xl font-bold tracking-tighter bg-gradient-to-r from-primary to-indigo-400 bg-clip-text text-transparent">
            CampusPulse
          </Link>
          <div className="hidden md:flex space-x-8">
            <a className="text-sm font-medium tracking-tight text-slate-600 hover:text-primary transition-colors" href="#features">Özellikler</a>
            <a className="text-sm font-medium tracking-tight text-slate-600 hover:text-primary transition-colors" href="#campus3d">3D Kampüs</a>
            <a className="text-sm font-medium tracking-tight text-slate-600 hover:text-primary transition-colors" href="#impact">Etki</a>
          </div>
          <div className="flex items-center space-x-4">
            <Link 
              to="/dashboard"
              className="text-sm font-medium tracking-tight px-6 py-2 rounded-full bg-gradient-to-r from-indigo-500 to-primary text-white shadow-lg shadow-primary/20 hover:opacity-80 transition-all duration-300 scale-95 hover:scale-100"
            >
              Panele Git
            </Link>
          </div>
        </div>
      </nav>

      <main className="flex-grow pt-24 pb-16">
        {/* Hero Section */}
        <section className="max-w-7xl mx-auto px-6 pt-16 pb-24 text-center">
          <h1 className="font-display text-5xl md:text-7xl mb-6 mx-auto max-w-4xl tracking-tight text-slate-900">
            Kampüs Enerji İsrafını{' '}
            <span className="bg-gradient-to-r from-primary to-indigo-400 bg-clip-text text-transparent">
              Durdurun.
            </span>
          </h1>
          <p className="text-slate-600 max-w-2xl mx-auto mb-10 text-lg md:text-xl leading-relaxed">
            Üniversitenizi akıllı, yeşil bir kampüse dönüştürün. CampusPulse, yapay zeka ve 3D Dijital İkiz teknolojileriyle enerji kayıplarını tespit eder, karbon ayak izini azaltır ve tasarruf sağlar.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-4 mb-6">
            <Link
              to="/dashboard"
              className="font-label-sm px-8 py-4 rounded-full bg-primary text-white shadow-[0_8px_16px_rgba(70,72,212,0.25)] hover:shadow-[0_12px_24px_rgba(70,72,212,0.35)] hover:-translate-y-1 transition-all duration-300 w-full sm:w-auto text-center"
            >
              Panele Git
            </Link>
            <Link
              to="/dashboard/live-map"
              className="font-label-sm px-8 py-4 rounded-full border border-[#c7c4d7] text-slate-700 bg-white hover:bg-slate-50 transition-all duration-300 w-full sm:w-auto text-center"
            >
              Canlı 3D Haritayı Gör
            </Link>
          </div>
        </section>

        {/* ── Özellikler ──────────────────────────────── */}
        <section id="features" className="max-w-7xl mx-auto px-6 py-24">
          <h2 className="font-h1 text-center mb-4 text-slate-900">Özellikler</h2>
          <p className="text-center text-slate-500 mb-16 max-w-xl mx-auto">Zeka, altyapıyla buluşuyor. Kampüsünüzün enerji yönetimini bir üst seviyeye taşıyın.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Card 1 */}
            <div className="bg-white rounded-[32px] p-8 shadow-[0_10px_25px_-5px_rgba(0,0,0,0.02),0_8px_10px_-6px_rgba(0,0,0,0.02)] border border-white hover:-translate-y-2 hover:shadow-[0_20px_40px_-10px_rgba(0,0,0,0.08)] transition-all duration-300">
              <div className="w-12 h-12 bg-indigo-50 rounded-2xl flex items-center justify-center mb-6">
                <span className="material-symbols-outlined text-primary">view_in_ar</span>
              </div>
              <h3 className="font-h2 text-slate-900 mb-4">3D Dijital İkiz</h3>
              <p className="text-slate-600">Tüm fakültenizi 3 boyutlu olarak görselleştirin. Hangi odanın enerji israfı yaptığını binaların üzerindeki canlı göstergelerden anında görün.</p>
            </div>
            {/* Card 2 */}
            <div className="bg-white rounded-[32px] p-8 shadow-[0_10px_25px_-5px_rgba(0,0,0,0.02),0_8px_10px_-6px_rgba(0,0,0,0.02)] border border-white hover:-translate-y-2 hover:shadow-[0_20px_40px_-10px_rgba(0,0,0,0.08)] transition-all duration-300">
              <div className="w-12 h-12 bg-indigo-50 rounded-2xl flex items-center justify-center mb-6">
                <span className="material-symbols-outlined text-indigo-500">memory</span>
              </div>
              <h3 className="font-h2 text-slate-900 mb-4">Yapay Zeka Anomali Tespiti</h3>
              <p className="text-slate-600">Isolation Forest tabanlı makine öğrenmesi motoru, normal kullanım kalıplarını öğrenir ve unutulan klimalar veya projektörler gibi anomalileri otomatik işaretler.</p>
            </div>
            {/* Card 3 */}
            <div className="bg-white rounded-[32px] p-8 shadow-[0_10px_25px_-5px_rgba(0,0,0,0.02),0_8px_10px_-6px_rgba(0,0,0,0.02)] border border-white hover:-translate-y-2 hover:shadow-[0_20px_40px_-10px_rgba(0,0,0,0.08)] transition-all duration-300">
              <div className="w-12 h-12 bg-emerald-50 rounded-2xl flex items-center justify-center mb-6">
                <span className="material-symbols-outlined text-emerald-500">eco</span>
              </div>
              <h3 className="font-h2 text-slate-900 mb-4">Eko-Finansal Takip</h3>
              <p className="text-slate-600">Saatlik mali kayıpları (₺/saat) ve karbon ayak izini (kg CO₂) hassas doğrulukla takip edin. Oda bazlı maliyet raporları oluşturun.</p>
            </div>
          </div>
        </section>


        {/* ── 3D Kampüs Önizleme ──────────────────────── */}
        <section id="campus3d" className="max-w-7xl mx-auto px-6 py-16">
          <h2 className="font-h1 text-center mb-4 text-slate-900">3D Dijital İkiz Kampüs</h2>
          <p className="text-center text-slate-500 mb-10 max-w-xl mx-auto">Düzce Üniversitesi Mühendislik Fakültesi binalarının etkileşimli 3D modeli.</p>
          <div className="relative max-w-5xl mx-auto">
            <div className="absolute -inset-1 bg-gradient-to-r from-primary to-indigo-300 rounded-[32px] blur opacity-20"></div>
            <div className="relative bg-white rounded-[32px] p-2 shadow-[0_10px_25px_-5px_rgba(0,0,0,0.05)] border border-white overflow-hidden">
              <div className="relative h-[500px] rounded-[28px] overflow-hidden bg-[#f5f2fe]">
                <Suspense fallback={
                  <div className="flex h-full items-center justify-center">
                    <div className="flex flex-col items-center gap-3">
                      <span className="material-symbols-outlined animate-spin text-4xl text-primary">autorenew</span>
                      <p className="text-sm text-slate-500">3D Kampüs yükleniyor...</p>
                    </div>
                  </div>
                }>
                  <ThreeDMap />
                </Suspense>
                <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-10">
                  <span className="text-white font-label-sm bg-black/50 px-4 py-2 rounded-full backdrop-blur-md text-xs">
                    🖱 Sürükle: Döndür · Kaydır: Yakınlaştır
                  </span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── Düzce Üniversitesi Enerji Verileri ──────── */}
        <section id="impact" className="max-w-7xl mx-auto px-6 py-12">
          <h2 className="font-h1 text-center mb-4 text-slate-900">Düzce Üniversitesi Enerji Profili</h2>
          <p className="text-center text-slate-500 mb-10 max-w-xl mx-auto">Gerçek kampüs verileriyle enerji tüketimi ve tasarruf potansiyeli.</p>
          <div className="bg-gradient-to-r from-indigo-50 to-emerald-50 rounded-[32px] p-12 md:p-16 border border-white/50 shadow-sm relative overflow-hidden">
            <div className="absolute inset-0 bg-white/20 backdrop-blur-[2px]"></div>
            <div className="relative z-10 grid grid-cols-1 md:grid-cols-4 gap-8 text-center divide-y md:divide-y-0 md:divide-x divide-slate-200/50">
              <div className="py-4 md:py-0">
                <div className="font-display text-4xl md:text-5xl text-primary mb-2">4.17M</div>
                <div className="font-label-sm text-slate-600 uppercase tracking-wider">Yıllık Tüketim (kWh)</div>
                <p className="text-xs text-slate-400 mt-2">Düzce Üniversitesi toplam</p>
              </div>
              <div className="py-4 md:py-0">
                <div className="font-display text-4xl md:text-5xl text-red-500 mb-2">₺10.4M</div>
                <div className="font-label-sm text-slate-600 uppercase tracking-wider">Tahmini Yıllık Maliyet</div>
                <p className="text-xs text-slate-400 mt-2">2.50 ₺/kWh birim fiyatıyla</p>
              </div>
              <div className="py-4 md:py-0">
                <div className="font-display text-4xl md:text-5xl text-emerald-600 mb-2">1,879</div>
                <div className="font-label-sm text-slate-600 uppercase tracking-wider">Ton CO₂ Emisyon</div>
                <p className="text-xs text-slate-400 mt-2">0.45 kg CO₂/kWh faktörüyle</p>
              </div>
              <div className="py-4 md:py-0">
                <div className="font-display text-4xl md:text-5xl text-indigo-600 mb-2">%30</div>
                <div className="font-label-sm text-slate-600 uppercase tracking-wider">2030 Tasarruf Hedefi</div>
                <p className="text-xs text-slate-400 mt-2">~1.25M kWh/yıl (Genelge 2023/15)</p>
              </div>
            </div>
          </div>
          {/* Genelge Notu */}
          <div className="mt-6 flex items-start gap-3 rounded-2xl bg-indigo-50/60 border border-indigo-100 px-6 py-4">
            <span className="material-symbols-outlined text-primary mt-0.5 text-[20px]">gavel</span>
            <p className="text-sm text-slate-600 leading-relaxed">
              <strong className="text-slate-800">2023/15 Sayılı Cumhurbaşkanlığı Genelgesi:</strong>{' '}
              Düzce Üniversitesi, ulusal enerji verimliliği hedefleri doğrultusunda 2030'a kadar elektrik tüketiminde en az %30 (yaklaşık 1.25 milyon kWh/yıl — eğitim binaları bazında) tasarruf sağlamakla yükümlüdür.
            </p>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-slate-50 w-full rounded-t-[32px] border-t border-slate-200 flex flex-col items-center px-8 py-10 mt-auto">
        <div className="text-lg font-bold bg-gradient-to-r from-primary to-indigo-400 bg-clip-text text-transparent mb-3">
          CampusPulse
        </div>
        <div className="text-xs text-slate-500">
          © 2026 CampusPulse. Tüm hakları saklıdır.
        </div>
      </footer>
    </div>
  );
}
