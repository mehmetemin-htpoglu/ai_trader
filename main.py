import yfinance as yf
import ollama

def borsa_analizi_yap(hisse_kodu):
    # 1. VERİ ÇEKME: Son 5 günlük hareketleri alalım
    hisse = yf.Ticker(hisse_kodu)
    gecmis_veriler = hisse.history(period="5d")
    
    # Veriyi metin haline getirelim (LLM'in okuyabilmesi için)
    ozet_veri = gecmis_veriler[['Close', 'Volume']].to_string()
    
    # 2. PROMPT (TALİMAT) HAZIRLAMA
    prompt = f"""
    Sen profesyonel bir yatırım danışmanısın. 
    Aşağıdaki {hisse_kodu} kodlu hissenin son 5 günlük kapanış fiyatları ve hacim verileri var:
    
    {ozet_veri}
    
    Bu verileri analiz et. Fiyat trendi ne yönde? Hacim artışları neyi işaret ediyor olabilir? 
    Kısa bir analiz yap ve "Yatırım Tavsiyesi Değildir" notuyla görüşünü bildir.
    """

    # 3. LLM'E SORMA (Ollama üzerinden)
    response = ollama.chat(model='deepseek-r1:8b', messages=[
        {'role': 'user', 'content': prompt},
    ])

    return response['message']['content']

# Test edelim (Örn: NVIDIA - NVDA veya Türk Hava Yolları - THYAO.IS)
print(borsa_analizi_yap("NVDA"))