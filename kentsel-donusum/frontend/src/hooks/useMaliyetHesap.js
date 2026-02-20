import { useState, useCallback } from 'react';

export function useMaliyetHesap() {
    const [hesapSonucu, setHesapSonucu] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const calculate = useCallback(async (payload) => {
        setLoading(true);
        setError(null);
        try {
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const res = await fetch(`${API_URL}/api/v1/hesapla`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                let errMsg = 'Hesaplama sırasında bir hata oluştu.';
                try {
                    const errData = await res.json();
                    errMsg = errData.detail || errMsg;
                } catch (e) { }
                throw new Error(errMsg);
            }

            const data = await res.json();
            setHesapSonucu(data);
        } catch (err) {
            setError(err.message);
            setHesapSonucu(null);
        } finally {
            setLoading(false);
        }
    }, []);

    return { hesapSonucu, loading, error, calculate };
}
