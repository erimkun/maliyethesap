import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function AdminPanel() {
    const [activeTab, setActiveTab] = useState('imar');
    const [message, setMessage] = useState({ type: '', text: '' });
    const [loading, setLoading] = useState(false);

    // Imar State
    const [imarForm, setImarForm] = useState({
        ada_no: '', parsel_no: '', taks: '', kaks: '',
        bagimsiz_bolum_sayisi: '', yapi_nizam: 'ayrik', yapi_sinifi: 'normal', imar_notlari: ''
    });

    // Tarife State
    const [tarifeForm, setTarifeForm] = useState({
        yil: 2025, ruhsat_harci_tl_m2: '', altyapi_payi_tl_m2: '', otopark_bedeli_tl: ''
    });

    // İstatistik State
    const [istatistik, setIstatistik] = useState(null);

    const navigate = useNavigate();
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    useEffect(() => {
        if (activeTab === 'istatistik' && !istatistik) {
            fetchIstatistik();
        }
    }, [activeTab]);

    const fetchIstatistik = async () => {
        try {
            const res = await fetch(`${API_URL}/api/v1/admin/istatistik`);
            const data = await res.json();
            setIstatistik(data);
        } catch (err) {
            console.error(err);
        }
    };

    const showMsg = (type, text) => {
        setMessage({ type, text });
        setTimeout(() => setMessage({ type: '', text: '' }), 3000);
    };

    const handleImarSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const payload = {
                ...imarForm,
                taks: parseFloat(imarForm.taks),
                kaks: parseFloat(imarForm.kaks),
                bagimsiz_bolum_sayisi: parseInt(imarForm.bagimsiz_bolum_sayisi, 10)
            };

            const res = await fetch(`${API_URL}/api/v1/admin/imar`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!res.ok) throw new Error("Kaydetme başarisiz!");
            showMsg('success', 'İmar bilgisi başarıyla kaydedildi.');
            setImarForm({ ada_no: '', parsel_no: '', taks: '', kaks: '', bagimsiz_bolum_sayisi: '', yapi_nizam: 'ayrik', yapi_sinifi: 'normal', imar_notlari: '' });
        } catch (err) {
            showMsg('error', err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleTarifeSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const payload = {
                yil: parseInt(tarifeForm.yil, 10),
                ruhsat_harci_tl_m2: parseFloat(tarifeForm.ruhsat_harci_tl_m2),
                altyapi_payi_tl_m2: parseFloat(tarifeForm.altyapi_payi_tl_m2),
                otopark_bedeli_tl: parseFloat(tarifeForm.otopark_bedeli_tl)
            };

            const res = await fetch(`${API_URL}/api/v1/admin/tarife`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!res.ok) throw new Error("Güncelleme başarısız!");
            showMsg('success', 'Tarife başarıyla güncellendi.');
        } catch (err) {
            showMsg('error', err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col items-center py-10 font-sans">
            <div className="w-full max-w-4xl bg-white rounded-xl shadow-lg flex flex-col overflow-hidden">

                {/* Header */}
                <div className="bg-blue-700 text-white p-6 flex justify-between items-center">
                    <div>
                        <h1 className="text-2xl font-bold">Belediye Yönetim Paneli</h1>
                        <p className="text-blue-100 text-sm mt-1">Sistem verilerini yapılandırın ve gözlemleyin</p>
                    </div>
                    <button onClick={() => navigate('/')} className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded font-medium transition text-sm">
                        Haritaya Dön
                    </button>
                </div>

                {/* Tab Navigation */}
                <div className="flex border-b border-gray-200">
                    <button onClick={() => setActiveTab('imar')} className={`flex-1 py-4 text-sm font-semibold text-center transition ${activeTab === 'imar' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500 hover:bg-gray-50'}`}>İmar Verisi Girişi</button>
                    <button onClick={() => setActiveTab('tarife')} className={`flex-1 py-4 text-sm font-semibold text-center transition ${activeTab === 'tarife' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500 hover:bg-gray-50'}`}>Tarife Güncelleme</button>
                    <button onClick={() => setActiveTab('istatistik')} className={`flex-1 py-4 text-sm font-semibold text-center transition ${activeTab === 'istatistik' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500 hover:bg-gray-50'}`}>Sorgulama İstatistikleri</button>
                </div>

                {/* Cihaz Ortası Body */}
                <div className="p-8 pb-10 flex-1 relative">

                    {message.text && (
                        <div className={`mb-6 p-4 rounded text-sm ${message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                            {message.text}
                        </div>
                    )}

                    {/* SEKME 1: Imar Verisi */}
                    {activeTab === 'imar' && (
                        <form onSubmit={handleImarSubmit} className="space-y-6 animate-fadeIn">
                            <div className="grid grid-cols-2 gap-6">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Ada No</label>
                                    <input type="text" required value={imarForm.ada_no} onChange={e => setImarForm({ ...imarForm, ada_no: e.target.value })} className="w-full border px-3 py-2 rounded focus:ring-2 outline-none focus:ring-blue-500" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Parsel No</label>
                                    <input type="text" required value={imarForm.parsel_no} onChange={e => setImarForm({ ...imarForm, parsel_no: e.target.value })} className="w-full border px-3 py-2 rounded focus:ring-2 outline-none focus:ring-blue-500" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">TAKS (0-1 arası)</label>
                                    <input type="number" step="0.01" min="0" max="1" required value={imarForm.taks} onChange={e => setImarForm({ ...imarForm, taks: e.target.value })} className="w-full border px-3 py-2 rounded focus:ring-2 outline-none focus:ring-blue-500" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">KAKS (0-10 arası)</label>
                                    <input type="number" step="0.05" min="0" max="10" required value={imarForm.kaks} onChange={e => setImarForm({ ...imarForm, kaks: e.target.value })} className="w-full border px-3 py-2 rounded focus:ring-2 outline-none focus:ring-blue-500" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Bağımsız Bölüm Sayısı</label>
                                    <input type="number" min="1" required value={imarForm.bagimsiz_bolum_sayisi} onChange={e => setImarForm({ ...imarForm, bagimsiz_bolum_sayisi: e.target.value })} className="w-full border px-3 py-2 rounded focus:ring-2 outline-none focus:ring-blue-500" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Yapı Nizamı</label>
                                    <select value={imarForm.yapi_nizam} onChange={e => setImarForm({ ...imarForm, yapi_nizam: e.target.value })} className="w-full border px-3 py-2 rounded focus:ring-2 outline-none focus:ring-blue-500">
                                        <option value="ayrik">Ayrık</option>
                                        <option value="bitisik">Bitişik</option>
                                        <option value="blok">Blok</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Yapı Sınıfı</label>
                                    <select value={imarForm.yapi_sinifi} onChange={e => setImarForm({ ...imarForm, yapi_sinifi: e.target.value })} className="w-full border px-3 py-2 rounded focus:ring-2 outline-none focus:ring-blue-500">
                                        <option value="luks">Lüks</option>
                                        <option value="normal">Normal</option>
                                        <option value="sosyal">Sosyal</option>
                                    </select>
                                </div>
                                {/* PDF Upload (görsel için) */}
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">İmar Planı PDF'si Yükle (LLM Parse)</label>
                                    <input type="file" accept=".pdf" className="w-full border px-3 py-2 rounded focus:ring-2 outline-none text-sm text-gray-500 file:mr-4 file:py-1 file:px-2 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
                                </div>
                            </div>

                            <div className="mt-4">
                                <label className="block text-sm font-medium text-gray-700 mb-1">İmar Notları</label>
                                <textarea rows="3" value={imarForm.imar_notlari} onChange={e => setImarForm({ ...imarForm, imar_notlari: e.target.value })} className="w-full border px-3 py-2 rounded focus:ring-2 outline-none focus:ring-blue-500" placeholder="Opsiyonel ek koşullar..."></textarea>
                            </div>

                            <button type="submit" disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded transition flex justify-center items-center mt-4">
                                {loading ? 'Kaydediliyor...' : 'İmar Verisini Kaydet'}
                            </button>
                        </form>
                    )}

                    {/* SEKME 2: Tarife Guncelleme */}
                    {activeTab === 'tarife' && (
                        <form onSubmit={handleTarifeSubmit} className="space-y-6 animate-fadeIn max-w-lg mx-auto">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Uygulama Yılı</label>
                                <select value={tarifeForm.yil} onChange={e => setTarifeForm({ ...tarifeForm, yil: e.target.value })} className="w-full border px-3 py-2 rounded focus:ring-2 outline-none focus:ring-blue-500">
                                    <option value="2024">2024</option>
                                    <option value="2025">2025</option>
                                    <option value="2026">2026</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Ruhsat Harcı (TL/m²)</label>
                                <input type="number" step="0.01" required value={tarifeForm.ruhsat_harci_tl_m2} onChange={e => setTarifeForm({ ...tarifeForm, ruhsat_harci_tl_m2: e.target.value })} className="w-full border px-3 py-2 rounded focus:ring-2 outline-none focus:ring-blue-500" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Altyapı Katılım Payı (TL/m²)</label>
                                <input type="number" step="0.01" required value={tarifeForm.altyapi_payi_tl_m2} onChange={e => setTarifeForm({ ...tarifeForm, altyapi_payi_tl_m2: e.target.value })} className="w-full border px-3 py-2 rounded focus:ring-2 outline-none focus:ring-blue-500" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Otopark Bedeli (TL Sabit)</label>
                                <input type="number" step="0.01" required value={tarifeForm.otopark_bedeli_tl} onChange={e => setTarifeForm({ ...tarifeForm, otopark_bedeli_tl: e.target.value })} className="w-full border px-3 py-2 rounded focus:ring-2 outline-none focus:ring-blue-500" />
                            </div>
                            <button type="submit" disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded transition flex justify-center items-center mt-6">
                                {loading ? 'Güncelleniyor...' : 'Tarife Güncelle'}
                            </button>
                        </form>
                    )}

                    {/* SEKME 3: Istatistik */}
                    {activeTab === 'istatistik' && (
                        <div className="animate-fadeIn max-w-2xl mx-auto text-gray-800">
                            {istatistik ? (
                                <>
                                    <div className="bg-blue-50 rounded-xl p-6 text-center shadow-sm border border-blue-100 mb-8">
                                        <span className="block text-sm font-semibold text-blue-600 uppercase tracking-widest mb-1">Son 7 Gün Sorgu Sayısı</span>
                                        <span className="text-5xl font-black text-blue-800">{istatistik.son_7_gun_sorgu_sayisi}</span>
                                    </div>

                                    <h3 className="font-bold text-lg mb-4 text-gray-700 border-b pb-2">En Çok Sorgulanan Mahalleler</h3>
                                    <div className="space-y-3">
                                        {istatistik.en_cok_sorgulanan_mahalleler.map((m, idx) => (
                                            <div key={idx} className="flex justify-between items-center bg-white p-4 border rounded-lg shadow-sm">
                                                <span className="font-medium text-gray-800">{idx + 1}. {m.mahalle}</span>
                                                <span className="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-sm font-semibold">{m.adet} Sorgu</span>
                                            </div>
                                        ))}
                                    </div>
                                </>
                            ) : (
                                <div className="text-center text-gray-500 py-10">İstatistikler yükleniyor...</div>
                            )}
                        </div>
                    )}

                </div>
            </div>
        </div>
    );
}
