from textwrap import dedent

__all__ = ['NOTIFY_RUNNING', 'NOTIFY_LOGIN', 'LOGIN_SUCCESS', 'LOGIN_FAILED', 'BUY_SIGNAL',
           'SELL_SIGNAL', 'BUY_FAILED_SIGNAL', 'BUY_FAILED_UPDATE', 'SELL_FAILED_SIGNAL', 'SELL_FAILED_UPDATE', 'DEFAULT_MESSAGE']

NOTIFY_RUNNING = '''
📢📢📢
BOT của **{username}** đã chạy vào lúc **{time}**
'''

NOTIFY_LOGIN = '''
📢📢📢
🚨 *Thông báo đăng nhập*!
💬 Tài khoản **{user_account}** chưa thực hiện đăng nhập vào **{platform_trading}**!

Vui lòng đăng nhập để thực hiện giao dịch từ bot!
'''

LOGIN_SUCCESS = '''
🔒🔒🔒 
🟢 **Đăng nhập thành công**! 🎉🎉🎉
🎉 Tài khoản **{user_account}** đã đăng nhập thành công vào **{platform_trading}**!

Bắt đầu chuẩn bị cho các giao dịch sắp tới! 🚀🚀🚀
'''

LOGIN_FAILED = '''
🛑🛑🛑
🔴 **Đăng nhập thất bại**! 🚫 🚫 🚫 
⚠️ Quá trình đăng nhập vào tài khoản **{user_account}** trên nền tảng **{platform_trading}** gặp sự cố!

Vui lòng kiểm tra lại thông tin và thử lại sau.
'''
SESSION_FAILED = '''
🛑🛑🛑
🔴 **Bot trading chưa hoạt động**! 🚫 🚫 🚫 
⚠️ Session_id **{session_id}** chưa hợp lệ. Vui lòng nhập lại mã session!
'''


BUY_SIGNAL = dedent('''
📈📈📈
🔔 **Tín hiệu MUA**:
- **Cổ phiếu**: **{stock}**
- **Lí do VNINDEX**: {message_vnindex}
- **Lí do STOCK**: {message}
''')

BUY_REQUEST_SIGNAL = dedent('''
📈📈📈
🔔 **Tín hiệu MUA TAY**:
- **Cổ phiếu**: **{stock}**
- **Level**: **{level}**
- **Lí do**: {message}
''')

BUY_ORDER_OVERRAL = dedent('''
💰💰💰 *{start_time_order}*
🔔 **Tài khoản {user_account}**:
- Lệnh MUA: **{stock}**
- Khối lượng mua dự kiến: **{volume}**
- **Level**: **{level}**
- **Giá hiện tại**: **{current_price}**
- Giá khởi đầu: **{start_price}**
- Số lượng lệnh  dự kiến: **{number_order}**
- Bước nhảy giá: **{step_price}**
- Biên trượt: **{slippage_buy}**
- Sai số giá đặt lệnh: **{add_price_buy}**
- Giá mua tối đa: **{limit_price}**
- Thời gian sửa một lệnh: **{sleeping_time_buy}** giây
''')
BUY_UPDATE_OVERRAL = dedent('''
💰💰💰 *{start_time_order}*
🔔 **Tài khoản {user_account}**:
- Sửa lệnh mua lần thứ **{times_update}**: **{stock}**
- Số lượng lệnh dự kiến: **{number_order}**
''')
BUY_CANCEL_OVERRAL = dedent('''
💰💰💰 *{start_time_order}*
🔔 **Tài khoản {user_account}**:
- Hủy lệnh mua: **{stock}**
- Lí do: **{reason}**
- Số lượng lệnh dự kiến: **{number_order}**
''')

BUY_MATCHED_OVERRAL = dedent('''
💰💰💰 *{start_time_order}*
🔔 **Tài khoản {user_account}**:
- Các lệnh mua đã khớp: **{stock}**
- Số lượng lệnh: **{number_order}**
''')

BUY_ORDER_DETAIL = '''
Lệnh MUA: **{stock}** - Giá: **{price}** - KL: **{volume}** - Trạng thái: **{status}**
'''
BUY_UPDATE_DETAIL = '''
Sửa lệnh  MUA: **{stock}** - Giá cũ: **{old_price}** - Giá mới: **{update_price}** - KL: **{volume}** - Trạng thái: **{status}**
'''
BUY_CANCEL_DETAIL = '''
Hủy lệnh  MUA: **{stock}** - Giá: **{price}** - KL: **{volume}** - Trạng thái: **{status}**
'''
BUY_MATCHED_DETAIL = '''
Lệnh  MUA: **{stock}** - Giá: **{price}** - KL: **{volume}** - Trạng thái: **{status}**
'''

SELL_SIGNAL = dedent('''
📉📉📉
🔔 **Tín hiệu BÁN**:
- **Cổ phiếu**: **{stock}**
- **Lí do**: {message}
''')
SELL_REQUEST_SIGNAL = dedent('''
📉📉📉
🔔 **Tín hiệu BÁN TAY**:
- **Cổ phiếu**: **{stock}**
- **Lí do**: {message}
''')
SELL_ORDER_OVERRAL = dedent('''
💰💰💰 *{start_time_order}*
🔔 **Tài khoản {user_account}**:
- Lệnh BÁN: **{stock}**
- Khối lượng bán dự kiến: **{volume}**
- **Giá hiện tại**: **{current_price}**
- Giá khởi đầu: **{start_price}**
- Bước nhảy giá: **{step_price}**
- Số lượng lệnh dự kiến: **{number_order}**
- Biên trượt: **{slippage_sell}**
- Sai số giá đặt lệnh: **{add_price_sell}**
- Giá bán tối thiểu: **{limit_price}**
- Thời gian sửa một lệnh: **{sleeping_time_sell}** giây
''')
SELL_UPDATE_OVERRAL = dedent('''
💰💰💰 *{start_time_order}*
🔔 **Tài khoản {user_account}**:
- Sửa lệnh bán lần thứ **{times_update}**: **{stock}**
- Số lượng lệnh dự kiến: **{number_order}**
''')
SELL_CANCEL_OVERRAL = dedent('''
💰💰💰 *{start_time_order}*
🔔 **Tài khoản {user_account}**:
- Hủy lệnh bán: **{stock}**
- Lí do: **{reason}**
- Số lượng lệnh dự kiến: **{number_order}**
''')
SELL_MATCHED_OVERRAL = dedent('''
💰💰💰
🔔 **Tài khoản {user_account}**:
- Lệnh bán đã khớp: **{stock}**
- Số lượng lệnh: **{number_order}**
''')

SELL_ORDER_DETAIL = '''
Lệnh BÁN: **{stock}** - Giá: **{price}** - KL: **{volume}** - Trạng thái: **{status}**
'''
SELL_UPDATE_DETAIL = '''
Sửa lệnh BÁN: **{stock}** - Giá cũ: **{old_price}** - Giá mới: **{update_price}** - KL: **{volume}** - Trạng thái: **{status}**
'''
SELL_CANCEL_DETAIL = '''
Hủy lệnh BÁN: **{stock}** - Giá: **{price}** - KL: **{volume}** - Trạng thái: **{status}**
'''
SELL_MATCHED_DETAIL = '''
Lệnh BÁN: **{stock}** - Giá: **{price}** - KL: **{volume}** - Trạng thái: **{status}**
'''


BUY_FAILED_SIGNAL = dedent('''
📈📈📈 *{start_time_order}*
🛑 **Tín hiệu MUA** không thành công:
- **Tài khoản {user_account}**:
- **Cổ phiếu**: **{stock}**
- **Level**: **{level}**
- **Giá hiện tại**: **{current_price}**
- **Lí do VNINDEX:**{message_vnindex}
- **Lí do STOCK:** {message}
''')
BUY_REQUEST_FAILED_SIGNAL = dedent('''
📈📈📈 *{start_time_order}*
🛑 **Tín hiệu MUA TAY** không thành công:
- **Tài khoản {user_account}**:
- **Cổ phiếu**: **{stock}**    
- **Lí do:** {message}
''')

BUY_FAILED_UPDATE = dedent('''
📈📈📈
🔔 **Sửa lệnh MUA không thành công** ⛔⛔⛔
❌ - **Tài khoản {user_account}** đã **Hủy** đặt lệnh **MUA**!
- **Cổ phiếu**: **{stock}**
- **Lí do VNINDEX:** {message_vnindex}
- **Lí do STOCK:** {message}
''')

SELL_FAILED_SIGNAL = dedent('''
📉📉📉
🔔 **Tín hiệu BÁN không thành công** ⛔⛔⛔
- **Tài khoản {user_account}** 
- **Cổ phiếu**: **{stock}**
- **Lí do:** {message}
''')
SELL_REQUEST_FAILED_SIGNAL = dedent('''
📉📉📉
🔔 **Tín hiệu BÁN TAY không thành công** ⛔⛔⛔
- **Tài khoản {user_account}**
- **Cổ phiếu**: **{stock}**
- **Lí do:** {message}
''')
TAKE_PROFIT_FAILED_SIGNAL = dedent('''
📉📉📉
🔔 **Tín hiệu CHỐT LÃI không thành công** ⛔⛔⛔
- **Tài khoản {user_account}**
- **Cổ phiếu**: **{stock}**
- **Lí do:** {message}
''')

SELL_FAILED_UPDATE = dedent('''
📉📉📉
🔔 **Sửa lệnh BÁN không thành công** ⛔⛔⛔
❌ - **Tài khoản {user_account}** đã **Hủy** đặt lệnh **BÁN**!
- **Cổ phiếu**: **{stock}**
- **Lí do:** {message}
''')

TAKEPROFIT_SIGNAL = dedent('''
🎯🎯🎯
🔔 **Tín hiệu CHỐT LÃI** 🚀🚀🚀
🥇 - **Tài khoản {user_account}** đã đặt lệnh chốt lời!
- **Cổ phiếu**: **{stock}**
- Khối lượng: **{volume}**
- Giá: **{price}**
- Phương án chốt lãi: **{take_profit_type}**
- **Lí do:** {message}
''')

STOPLOSS_SIGNAL = dedent('''
🚨🚨🚨
🔔 **Tín hiệu CẮT LỖ** 💔💔💔
⚠️ - **Tài khoản {user_account}** trên **{platform_trading}** đã đặt lệnh cắt lỗ!
- **Cổ phiếu**: **{stock}**
- Khối lượng: **{volume}**
- Giá: **{price}**
- **Lí do:** {message}
''')

DEFAULT_MESSAGE = '''
❓❓❓
Tin nhắn mặc định của hệ thống!.

Chúc cho các giao dịch sắp tới thành công! 🚀🚀🚀
'''
