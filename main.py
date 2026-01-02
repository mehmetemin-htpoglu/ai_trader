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
    
    You are a professional investment advisor. 
    Below are the closing prices and volume data for the last 5 days for the stock with the code {hisse_kodu}:
    
    {ozet_veri}
    
    Analyze this data. What is the price trend? What might the volume increases indicate?
    Conduct a brief analysis and share your opinion with a "Not Investment Advice" note.
    """

    # 3. LLM'E SORMA (Ollama üzerinden)
    response = ollama.chat(model='deepseek-r1:8b', messages=[
        {'role': 'user', 'content': prompt},
    ])

    return response['message']['content']

# Test edelim (Örn: NVIDIA - NVDA veya Türk Hava Yolları - THYAO.IS)
print(borsa_analizi_yap("NVDA"))