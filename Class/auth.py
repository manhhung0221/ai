from manage_engine import engine_stockDB
from dotenv import load_dotenv
import os
load_dotenv()

class FireAnt:
    def __init__(self):
        FIREANT_TOKEN = os.getenv("FIREANT_TOKEN")
        self.token = FIREANT_TOKEN

    def headers(self):
        return {
            'Authorization': f'{self.token}',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        }
class FiinAuth:
    def __init__(self, host: str):
        self.host = host
        # self.token = token
        self.u0 = engine_stockDB.execute(f"SELECT key FROM public.auth_fiin").fetchone()[0]
    
    def headers(self):
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
            "Authorization": f"Bearer",
            "Connection": "keep-alive",
            "Host": self.host,
            "Origin": "https://fiintrade.vn",
            "Referer": "https://fiintrade.vn/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "u0": self.u0
        }

# Ví dụ sử dụng

