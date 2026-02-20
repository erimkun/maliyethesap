import { useState, useCallback } from 'react';

export function useParselSorgu() {
    const [parselData, setParselData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchParsel = useCallback(async (lat, lon) => {
        setLoading(true);
        setError(null);
        try {
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const res = await fetch(`${API_URL}/api/v1/parsel/${lat}/${lon}`);

            if (!res.ok) {
                let errMsg = 'Bir hata oluştu.';
                try {
                    const errData = await res.json();
                    errMsg = errData.detail || errMsg;
                } catch (e) { }
                throw new Error(errMsg);
            }

            const data = await res.json();
            setParselData(data);
        } catch (err) {
            setError(err.message);
            setParselData(null);
        } finally {
            setLoading(false);
        }
    }, []);

    return { parselData, loading, error, fetchParsel };
}
