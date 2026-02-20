import React, { useState, useEffect } from 'react';
import { useMaliyetHesap } from '../hooks/useMaliyetHesap';

export default function MaliyetPaneli({ parselData }) {
    const { hesapSonucu, loading, error, calculate } = useMaliyetHesap();

    const [formData, setFormData] = useState({
        kaks: parselData?.kaks || '2.0',
        taks: parselData?.taks || '0.4',
        bagimsiz_bolum_sayisi: parselData?.bagimsiz_bolum_sayisi || '8',
        yapi_sinifi: 'normal',
        arsa_payim_var: false,
        arsa_payi_pay: '',
        arsa_payi_payda: ''
    });

    // Eğer parselData değişirse formları güncelleme
    useEffect(() => {
        if (parselData) {
            setFormData(prev => ({
                ...prev,
                kaks: parselData.kaks || '2.0',
                taks: parselData.taks || '0.4',
                bagimsiz_bolum_sayisi: parselData.bagimsiz_bolum_sayisi || '8'
            }));
        }
    }, [parselData]);

    const handleChange = (e) => {
        const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
        setFormData({ ...formData, [e.target.name]: value });
    };

    const handleHesapla = () => {
        if (!parselData) return;

        // API için payload hazırlığı
        const payload = {
            parsel_alan_m2: parselData.alan_m2,
            kaks: formData.kaks,
            taks: formData.taks,
            bagimsiz_bolum_sayisi: parseInt(formData.bagimsiz_bolum_sayisi, 10),
            mevcut_yapi_alan_m2: parselData.alan_m2 * 0.8, // Geçiçi mock yaklaşım.
            yapi_sinifi: formData.yapi_sinifi,
            belediye_kodu: parselData.ilce.toLowerCase().replace('ü', 'u').replace('ö', 'o') || 'uskudar',
            arsa_payi_pay: formData.arsa_payim_var ? parseInt(formData.arsa_payi_pay, 10) : null,
            arsa_payi_payda: formData.arsa_payim_var ? parseInt(formData.arsa_payi_payda, 10) : null,
        };

        calculate(payload);
    };

    const formatCurrency = (val) => new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(val);

    return (
        <div className="bg-white w-96 max-w-full h-full flex flex-col border-l border-gray-200 overflow-y-auto z-10 p-5 shadow-xl">
            <h2 className="text-xl font-bold text-gray-800 mb-4 border-b pb-2">Dönüşüm Maliyet Hesaplama</h2>

            {/* 1. Parsel Bilgileri */}
            <section className="mb-6 bg-blue-50 p-3 rounded-lg border border-blue-100">
                <h3 className="font-semibold text-blue-800 text-sm mb-2">1. Seçilen Parsel Bilgileri</h3>
                {parselData ? (
                    <div className="text-sm text-gray-700 grid grid-cols-2 gap-2">
                        <div><span className="font-medium">İlçe:</span> {parselData.ilce}</div>
                        <div><span className="font-medium">Ada/Parsel:</span> {parselData.ada_no} / {parselData.parsel_no}</div>
                        <div><span className="font-medium">Alan (m²):</span> {parselData.alan_m2}</div>
                        <div><span className="font-medium">KAKS/TAKS:</span> {formData.kaks} / {formData.taks}</div>
                    </div>
                ) : (
                    <p className="text-sm text-gray-500 italic">Haritadan bir alan seçin.</p>
                )}
            </section>

            {/* 2. Kullanıcı Girdileri */}
            <section className="mb-6">
                <h3 className="font-semibold text-gray-800 text-sm mb-3">2. Bina Durumu</h3>
                <div className="space-y-3">
                    <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Bağımsız Bölüm (Daire) Sayısı</label>
                        <input type="number" name="bagimsiz_bolum_sayisi" value={formData.bagimsiz_bolum_sayisi} onChange={handleChange}
                            className="w-full px-3 py-2 border rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-500" />
                    </div>
                    <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">Yapı Sınıfı</label>
                        <select name="yapi_sinifi" value={formData.yapi_sinifi} onChange={handleChange}
                            className="w-full px-3 py-2 border rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="lüks">Lüks İnşaat</option>
                            <option value="normal">Normal İnşaat</option>
                            <option value="sosyal">Sosyal Konut</option>
                        </select>
                    </div>

                    <div className="pt-2">
                        <label className="flex items-center text-sm font-medium text-gray-700">
                            <input type="checkbox" name="arsa_payim_var" checked={formData.arsa_payim_var} onChange={handleChange}
                                className="mr-2 h-4 w-4 text-blue-600 rounded" />
                            Arsa payımı biliyorum
                        </label>
                    </div>

                    {formData.arsa_payim_var && (
                        <div className="flex gap-2">
                            <div className="flex-1">
                                <label className="block text-xs text-gray-500 mb-1">Pay</label>
                                <input type="number" name="arsa_payi_pay" placeholder="Örn: 80" value={formData.arsa_payi_pay} onChange={handleChange}
                                    className="w-full px-3 py-2 border rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-500" />
                            </div>
                            <div className="flex-1">
                                <label className="block text-xs text-gray-500 mb-1">Payda</label>
                                <input type="number" name="arsa_payi_payda" placeholder="Örn: 1000" value={formData.arsa_payi_payda} onChange={handleChange}
                                    className="w-full px-3 py-2 border rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-500" />
                            </div>
                        </div>
                    )}
                </div>
            </section>

            {/* 3. Hesapla Butonu */}
            <button
                onClick={handleHesapla}
                disabled={!parselData || loading}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-4 rounded-lg transition duration-200 mb-6 flex justify-center items-center"
            >
                {loading ? (
                    <span className="flex items-center gap-2">
                        <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Hesaplanıyor...
                    </span>
                ) : 'Dönüşüm Maliyetini Hesapla'}
            </button>

            {/* Error State */}
            {error && (
                <div className="p-3 bg-red-50 text-red-600 rounded border border-red-200 text-sm mb-4">
                    ⚠️ {error}
                </div>
            )}

            {/* 4. Sonuç Kartları */}
            {hesapSonucu && !loading && (
                <div className="space-y-3 pt-4 border-t border-gray-100 flex-1">
                    <div className="bg-orange-50 border border-orange-200 p-4 rounded-lg">
                        <h4 className="text-xs font-semibold text-orange-800 uppercase tracking-wider mb-1">Tahmini Toplam Maliyet</h4>
                        <div className="text-xl font-bold text-orange-600 mb-1">
                            {formatCurrency(hesapSonucu.guvenaraligi_alt_tl)} - {formatCurrency(hesapSonucu.guvenaraligi_ust_tl)}
                        </div>
                        <p className="text-[10px] text-orange-700 opacity-80">Rakamlar bina toplam yapım ortalamasıdır.</p>
                    </div>

                    <div className="bg-red-50 border border-red-200 p-4 rounded-lg">
                        <h4 className="text-xs font-semibold text-red-800 uppercase tracking-wider mb-1">Senin Payına Düşen</h4>
                        <div className="text-2xl font-black text-red-600">
                            {formatCurrency(hesapSonucu.kisi_payi_tl)}
                        </div>
                        <p className="text-[10px] text-red-700 opacity-80 mt-1">({hesapSonucu.arsa_payi_baz === 'arsa_payi' ? 'Arsa payına ' : 'Eşit '} göre hesaplanmıştır)</p>
                    </div>

                    <div className="bg-green-50 border border-green-200 p-4 rounded-lg">
                        <h4 className="text-xs font-semibold text-green-800 uppercase tracking-wider mb-1">Kat Karşılığı Senaryosu</h4>
                        <div className="text-lg font-bold text-green-700">
                            Yeni dairenizden <span className="text-green-900 border-b-2 border-green-300">{hesapSonucu.kat_karsiligi_daire_m2} m²</span> size kalır
                        </div>
                        <p className="text-[10px] text-green-700 opacity-80 mt-1">Müteahhit payı %40 baz alınmıştır.</p>
                    </div>

                    <p className="text-[10px] text-gray-400 text-center italic mt-4 pt-4 border-t">
                        ⚠️ Bu hesap tahmindir, yasal bağlayıcılığı yoktur. (Versiyon: {hesapSonucu.motor_versiyonu})
                    </p>
                </div>
            )}
        </div>
    );
}
