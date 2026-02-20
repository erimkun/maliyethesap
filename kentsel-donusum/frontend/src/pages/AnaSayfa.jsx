import React, { useState, useRef, useCallback } from 'react';
import Map, { Marker, NavigationControl } from 'react-map-gl';
import { MapPin } from 'lucide-react';
import MaliyetPaneli from '../components/MaliyetPaneli';
import { useParselSorgu } from '../hooks/useParselSorgu';

export default function AnaSayfa() {
    const mapRef = useRef(null);

    // Haritada seçili olan nokta konumu
    const [marker, setMarker] = useState(null);
    const { parselData, loading: parselLoading, error: parselError, fetchParsel } = useParselSorgu();

    const handleMapClick = useCallback((event) => {
        const { lng, lat } = event.lngLat;
        setMarker({ longitude: lng, latitude: lat });
        fetchParsel(lat, lng);
    }, [fetchParsel]);

    return (
        <div className="w-full h-screen flex flex-col md:flex-row overflow-hidden relative font-sans">

            {/* Sol Pane - Mapbox Harita */}
            <div className="flex-1 h-full w-full relative">
                <Map
                    ref={mapRef}
                    initialViewState={{
                        longitude: 29.03, // İstanbul merkez
                        latitude: 41.01,
                        zoom: 13
                    }}
                    mapStyle="mapbox://styles/mapbox/light-v11"
                    mapboxAccessToken={import.meta.env.VITE_MAPBOX_TOKEN}
                    onClick={handleMapClick}
                    cursor={parselLoading ? "wait" : "crosshair"}
                    interactiveLayerIds={['settlement-label', 'poi-label']} // Sadece tıklama referansı için
                >
                    <NavigationControl position="bottom-right" />

                    {marker && (
                        <Marker longitude={marker.longitude} latitude={marker.latitude} anchor="bottom">
                            <div className="animate-bounce">
                                <MapPin className="text-blue-600 w-8 h-8 fill-blue-100" />
                            </div>
                        </Marker>
                    )}

                    {/* Harita Overlay Loading State */}
                    {parselLoading && (
                        <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-white px-5 py-2 rounded-full shadow-lg border border-blue-100 text-sm font-semibold text-blue-800 flex items-center gap-2 z-10 transition-all">
                            <svg className="animate-spin h-4 w-4 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Parsel Aranıyor...
                        </div>
                    )}

                    {parselError && (
                        <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-red-50 px-5 py-2 rounded-full shadow-lg border border-red-200 text-sm font-semibold text-red-800 flex items-center gap-2 z-10">
                            ❌ {parselError}
                        </div>
                    )}
                </Map>
            </div>

            {/* Sağ Pane - Maliyet Formu */}
            <MaliyetPaneli parselData={parselData} />

        </div>
    );
}
