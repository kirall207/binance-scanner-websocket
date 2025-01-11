import os
import time
import asyncio
import numpy as np
import pandas as pd
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException
from websocket import WebSocketApp
from telegram.ext import Application
import json
from dotenv import load_dotenv
import logging
from collections import deque
import ta
from concurrent.futures import ProcessPoolExecutor

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# .env dosyasından çevre değişkenlerini yükle
load_dotenv()

# API bilgilerini al
API_KEY = os.getenv("BINANCE_API_KEY_6")
API_SECRET = os.getenv("BINANCE_API_SECRET_6")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN_4")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_GROUP_CHAT_ID_4")

# Sabitler
ZAMAN_DILIMLERI = ['15m', '1h', '4h']
HACIM_ESIGI = 1000000  # 1 milyon USDT
MAX_CANDLES = 100  # Tutulacak maksimum mum sayısı

class IndicatorCalculator:
    """Gösterge hesaplamaları için yardımcı sınıf"""
    
    @staticmethod
    def calculate_rsi(closes, period=14):
        """Numpy ile RSI hesapla"""
        delta = np.diff(closes)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        
        avg_gain = np.concatenate(([np.nan], np.convolve(gain, np.ones(period)/period, mode='valid')))
        avg_loss = np.concatenate(([np.nan], np.convolve(loss, np.ones(period)/period, mode='valid')))
        
        rs = avg_gain / np.where(avg_loss == 0, 1, avg_loss)
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
