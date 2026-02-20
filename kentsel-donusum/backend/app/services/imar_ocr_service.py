import os
import base64
import logging
import pdfplumber

logger = logging.getLogger(__name__)

class ImarOCRService:
    def __init__(self, llm_service):
        self.llm_service = llm_service

    async def pdf_isle(self, pdf_path: str, ada_no: str, parsel_no: str) -> dict:
        """
        PDF belgesini OCR veya saf metin çıkarma teknikleriyle okuyup
        yapılandırılmış imar notu (TAKS/KAKS vd.) olarak döndürür.
        """
        if not os.path.exists(pdf_path):
             return {"error": "Dosya bulunamadi"}
             
        text_content = self._pdf_metin_cek(pdf_path)
        
        # Eğer çıkarılan metin yeterliyse LLM'e yolla, OCR'ye gerek yok
        if len(text_content.strip()) > 100:
             logger.info("PDF'ten doğrudan metin okundu. LLM servisine aktarılıyor.")
             result = await self.llm_service.imar_notu_parse(text_content, ada_no, parsel_no)
             result['metod'] = 'pdf_text'
             return result
             
        # Tesseract veya Claude Vision gibi OCR metotlarına fall-back edilecek
        logger.info("Metin bulunamadı veya çok kısa. OCR taranmış resim (Tesseract/Vision) işareti alındı.")
        
        ocr_result_text = self._ocr_uygula(pdf_path)
        
        if len(ocr_result_text.strip()) > 50:
             result = await self.llm_service.imar_notu_parse(ocr_result_text, ada_no, parsel_no)
             result['metod'] = 'ocr'
             return result
             
        # Çok belirsiz ise (Mocklanmış Fallback - İleri Vision)
        return {"error": "OCR yetersiz, vision API kullanılmalı (Faz 3+)"}
        
    def _pdf_metin_cek(self, pdf_path: str) -> str:
        """pdfplumber kullanarak doğrudan text tabanlı PDF'lerden karakterleri çıkartır"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_pages = [page.extract_text() or '' for page in pdf.pages]
                return " ".join(text_pages)
        except Exception as e:
            logger.error(f"PDF metin okuma hatasi: {str(e)}")
            return ""

    def _ocr_uygula(self, pdf_path: str) -> str:
        """Kılavuzdaki taslak Tesseract kurgusu. OCR eklenebilir."""
        try:
           import pytesseract
           from pdf2image import convert_from_path
           
           images = convert_from_path(pdf_path, dpi=300)
           full_text = []
           for img in images:
               text = pytesseract.image_to_string(img, lang='tur', config='--psm 6')
               full_text.append(text)
           return " ".join(full_text)
        except ImportError:
           logger.warning("Pytesseract yuklenmedigi veya calismadigi icin OCR atlandi.")
           return ""
        except Exception as e:
           logger.error(f"OCR Pipeline hatasi: {str(e)}")
           return ""
