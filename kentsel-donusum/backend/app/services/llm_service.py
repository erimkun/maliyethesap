import os
import json
import logging
from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = AsyncAnthropic(api_key=self.api_key)

    async def imar_notu_parse(self, raw_text: str, ada_no: str, parsel_no: str) -> dict:
        """Claude modeline imar planı notlarını gönderip yapılandırılmış veri çeker."""
        if not self.api_key:
            logger.warning("Anthropic API key bulunamadi. LLM entegrasyonu calismayacak.")
            return {}
            
        system_prompt = (
            "Sen bir imar planı uzmanısın. Verilen metinden belirtilen ada/parsel için TAKS, KAKS, "
            "max_yukseklik_m, yapi_nizam (ayrik/bitisik/blok) ve ozel_kosullar'ı JSON formatında çıkar. "
            "Bulunmayanlar için null döndür. Sadece ve sadece geçerli bir JSON objesi döndür, "
            "başka bir açıklama metni ekleme."
        )
        
        user_prompt = f"Ada: {ada_no}, Parsel: {parsel_no}\n\nİmar Notları:\n{raw_text[:8000]}"
        
        try:
            response = await self.client.messages.create(
                model="claude-3-opus-20240229",
                system=system_prompt,
                max_tokens=1000,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            result_json = response.content[0].text
            return json.loads(result_json)
        except Exception as e:
            logger.error(f"Claude API (imar) hatasi: {str(e)}")
            return {"error": "LLM Hatasi"}

    async def bakanlik_cetveli_parse(self, tablo_metni: str) -> list[dict]:
        """PDF formatından çıkarılan yapı sınıfları ve birim bedelleri formatlar."""
        if not self.api_key:
             return []
             
        system_prompt = (
            "Bakanlık inşaat maliyet cetvesinden yapı sınıfı ve TL/m² değerlerini JSON array olarak çıkar. "
            "Format: [{'yapi_sinifi': str, 'birim_bedel_tl_m2': number}] "
            "Sadece JSON döndür."
        )
        
        try:
            response = await self.client.messages.create(
                model="claude-3-opus-20240229",
                system=system_prompt,
                max_tokens=1000,
                messages=[{"role": "user", "content": tablo_metni[:8000]}]
            )
            
            result_json = response.content[0].text
            return json.loads(result_json)
        except Exception as e:
            logger.error(f"Claude API (cetvel) hatasi: {str(e)}")
            return []
