import io
with io.open('apps/trading/service/helper.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the \'OFF\' issue
text = text.replace(r"\'OFF\'", "'OFF'")

# Also fix the weird indentation of the line before "if is_use_..."
text = text.replace(
    "                following_second, following_reasons_second = False, []",
    "        following_second, following_reasons_second = False, []"
)
text = text.replace(
    "            trading_second, trading_reasons_second = False, []",
    "        trading_second, trading_reasons_second = False, []"
)

with io.open('apps/trading/service/helper.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Fix completed")
