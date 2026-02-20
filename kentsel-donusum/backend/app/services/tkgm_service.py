import httpx
import logging

logger = logging.getLogger(__name__)

class TKGMService:
    async def koordinattan_parsel_bul(self, lat: float, lon: float) -> dict | None:
        """TKGM üzerinden koordinattan parsel sorgular. EPSG:4326 kullanır."""
        base_url = "https://atlas.tkgm.gov.tr/mapcache/wms"
        bbox = f"{lon-0.001},{lat-0.001},{lon+0.001},{lat+0.001}"
        
        params = {
            'SERVICE': 'WMS',
            'VERSION': '1.1.1',
            'REQUEST': 'GetFeatureInfo',
            'LAYERS': 'parsel',
            'QUERY_LAYERS': 'parsel',
            'INFO_FORMAT': 'application/json',
            'SRS': 'EPSG:4326',
            'BBOX': bbox,
            'WIDTH': '101',
            'HEIGHT': '101',
            'X': '50',
            'Y': '50',
            'FEATURE_COUNT': '1'
        }
        
        async with httpx.AsyncClient() as client:
            try:
                # 3 kez deneme yapılabilir ama timeout'la basite indirgiyorum
                response = await client.get(base_url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                features = data.get("features", [])
                
                if features:
                    props = features[0].get("properties", {})
                    return {
                        'ada_no': str(props.get('adaNo', props.get('ada', ''))),
                        'parsel_no': str(props.get('parselNo', props.get('parsel', ''))),
                        'ilce': str(props.get('ilceAd', props.get('ilce', ''))),
                        'il': str(props.get('ilAd', props.get('il', ''))),
                        'alan_m2': props.get('tapuAlan', props.get('alan', 0))
                    }
            except Exception as e:
                logger.error(f"TKGM WMS hatasi: {str(e)}")
                return None
                
        return None
