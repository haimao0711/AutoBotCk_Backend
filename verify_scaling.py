import pandas as pd
from datetime import datetime
import pytz

# Enum Mock
class CandleEnum:
    M5 = 'M5'

def patch_realtime_data_with_normalization(df, match_price, chart_type):
    if df is None or df.empty:
        return

    try:
        # Normalization Logic
        last_idx = df.index[-1]
        last_close = df.at[last_idx, 'close']
        
        # Heuristic: If discrepancy is > 100x, assume unit mismatch
        ratio = match_price / last_close if last_close != 0 else 0
        
        normalized_price = match_price
        if ratio > 100:
            print(f"⚠️ Detect Unit Mismatch: match_price ({match_price}) vs last_close ({last_close}). Ratio {ratio:.2f}. Dividing by 1000.")
            normalized_price = match_price / 1000
        elif ratio < 0.01:
             print(f"⚠️ Detect Unit Mismatch: match_price ({match_price}) vs last_close ({last_close}). Ratio {ratio:.2f}. Multiplying by 1000.")
             normalized_price = match_price * 1000
        
        match_price = normalized_price

        # timezone
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(tz)
        
        # Mocking time for test consistency
        # Assuming current time is same as last candle for UPDATE test
        current_candle_ts = int(df.at[last_idx, 'time']) 
        last_ts = int(df.at[last_idx, 'time'])
        
        if last_ts == current_candle_ts:
            df.at[last_idx, 'close'] = match_price
            df.at[last_idx, 'high'] = max(df.at[last_idx, 'high'], match_price)
            df.at[last_idx, 'low'] = min(df.at[last_idx, 'low'], match_price)
            
    except Exception as e:
        print(f"Error: {e}")

def test_scaling():
    # Scenario: Historical data is in thousands (30.0), Realtime is raw (30000)
    df = pd.DataFrame([{
        'time': 1700000000,
        'close': 30.5,
        'high': 30.6,
        'low': 30.4,
        'open': 30.5,
        'volume': 1000,
        'id': 1
    }])
    
    raw_realtime_price = 31000 # 31.0
    
    print(f"Test 1: Normalization Check. Hist: 30.5, Realtime: {raw_realtime_price}")
    patch_realtime_data_with_normalization(df, raw_realtime_price, CandleEnum.M5)
    
    final_close = df.iloc[-1]['close']
    print(f"Result Close: {final_close}")
    
    if 30 < final_close < 32:
        print("✅ Normalization Success")
    else:
        print("❌ Normalization Failed")

if __name__ == "__main__":
    test_scaling()
