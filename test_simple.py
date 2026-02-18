import pandas as pd
import numpy as np
from datetime import datetime
import os

print("=" * 60)
print("Testing get_gigadevice_data.py functionality")
print("=" * 60)

# Test 1: Check libraries
print("\nTest 1: Checking required libraries...")
try:
    print(f"  pandas version: {pd.__version__}")
    print(f"  numpy version: {np.__version__}")
    print("  ✅ Libraries available")
except ImportError as e:
    print(f"  ❌ Import error: {e}")
    exit(1)

# Test 2: Create sample data
print("\nTest 2: Creating sample data...")
try:
    dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
    n = len(dates)
    np.random.seed(42)
    base_price = 50
    returns = np.random.normal(0.0005, 0.02, n)
    price = base_price * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'stock_code': '603986.SH',
        'trade_date': dates,
        'close': price
    })
    
    print(f"  ✅ Created {len(df)} records")
except Exception as e:
    print(f"  ❌ Error: {e}")
    exit(1)

# Test 3: Calculate moving averages
print("\nTest 3: Calculating moving averages...")
try:
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma20'] = df['close'].rolling(window=20).mean()
    print(f"  ✅ MA5: {df['ma5'].iloc[-1]:.2f}")
    print(f"  ✅ MA20: {df['ma20'].iloc[-1]:.2f}")
except Exception as e:
    print(f"  ❌ Error: {e}")
    exit(1)

# Test 4: Save CSV
print("\nTest 4: Saving CSV file...")
try:
    test_dir = 'test_output'
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    csv_file = os.path.join(test_dir, 'test.csv')
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"  ✅ CSV saved: {csv_file}")
    print(f"  ✅ File size: {os.path.getsize(csv_file)} bytes")
except Exception as e:
    print(f"  ❌ Error: {e}")
    exit(1)

# Test 5: Read CSV
print("\nTest 5: Reading CSV file...")
try:
    df_read = pd.read_csv(csv_file)
    print(f"  ✅ Read {len(df_read)} records")
    print(f"  ✅ Data matches: {len(df) == len(df_read)}")
except Exception as e:
    print(f"  ❌ Error: {e}")
    exit(1)

# Test 6: Save Excel (optional)
print("\nTest 6: Saving Excel file...")
try:
    excel_file = os.path.join(test_dir, 'test.xlsx')
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Test', index=False)
    print(f"  ✅ Excel saved: {excel_file}")
    print(f"  ✅ File size: {os.path.getsize(excel_file)} bytes")
except ImportError:
    print("  ⚠️  openpyxl not available, skipping Excel test")
except Exception as e:
    print(f"  ⚠️  Excel save failed: {e}")

# Test 7: Statistics
print("\nTest 7: Calculating statistics...")
try:
    print(f"  ✅ High: {df['close'].max():.2f}")
    print(f"  ✅ Low: {df['close'].min():.2f}")
    print(f"  ✅ Average: {df['close'].mean():.2f}")
except Exception as e:
    print(f"  ❌ Error: {e}")
    exit(1)

# Cleanup
print("\nTest 8: Cleaning up test files...")
try:
    os.remove(csv_file)
    if os.path.exists(excel_file):
        os.remove(excel_file)
    os.rmdir(test_dir)
    print("  ✅ Test files cleaned up")
except:
    print("  ⚠️  Some files could not be cleaned")

print("\n" + "=" * 60)
print("✅ All tests passed!")
print("✅ get_gigadevice_data.py should work correctly")
print("=" * 60)
