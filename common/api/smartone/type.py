from typing import List, Optional
from dataclasses import dataclass
from typing import Optional
from typing import TypedDict, List


class ResponseSmartOneType(TypedDict):
    cmd: str
    oID: str
    rc: int
    rs: str
    data: List


@dataclass
class Order:
    ROW_NUM: float
    PK_ORDER: str
    C_ORDER_NO: float
    C_ACCOUNT_CODE: str
    C_SHARE_CODE: str
    C_SIDE: str
    C_SIDE_TYPE: Optional[str]
    C_CHANEL: str
    C_CHANEL_NAME: str
    C_ORDER_DATE: str
    C_ORDER_TIME: str
    C_ORDER_VOLUME: float
    C_ORDER_PRICE: float
    C_ORDER_STATUS: str
    C_SHOW_STATUS: str
    C_STATUS_NAME: str
    C_STATUS_NAME_EN: str
    C_SHOW_PRICE: str
    C_SET_ORDER_TYPE: str
    C_CONFIRM_STATUS: str
    C_CONFIRM_TIME: Optional[str]
    C_MATCH_VOL: float
    C_UNMATCH_VOL: float
    C_MATCH_PRICE: float
    C_FEE_VALUE: float
    C_TAX_VALUE: float
    C_MATCHED_VALUE: float
    C_DIV_TAX_VALUE: float
    C_CANCEL_TIME: Optional[str]
    C_MATCHED_TIME: Optional[str]
    C_ORDER_TYPE: str
    C_ORDER_TYPE_NAME: str
    C_TOTAL_RECORD: float


@dataclass
class ListOrderResponse:
    cmd: str
    oID: str
    rc: int
    rs: Optional[str]
    data: List[Order]


@dataclass
class OrderData:
    symbol: str
    shareStatus: str
    status: str
    msg_type: str
    showPrice: str
    orderTime: str
    type: str
    accountCode: str
    orderNo: int
    market: str
    matchVolume: int
    side: str
    volume: str
    pk_orderNo: str
    order_out_room: str
    channel: str
    refID: str
    group: str
    autoType: Optional[str]
    product: Optional[str]


@dataclass
class UpdateOrderData:
    orderNo: int
    msg_type: str
    status: str
    showPrice: float
    volume: int
    pk_orderNo: int


@dataclass
class CancelOrderData:
    orderNo: int
    msg_type: str
    status: str
    pk_orderNo: int


@dataclass
class StockData:
    symbol: str
    share_status: str
    actual_vol: int
    actual_vol_02: int
    avaiable_vol: int
    avaiable_vol_fs: int
    repo_vol: int
    right_vol: int
    other_vol: int
    margin_rate: int
    buy_t1: int
    sell_t1: int
    buy_t2: int
    sell_t2: int
    buy_t0: int
    sell_t0: int
    account: str
    sell_unmatch_vol: int
    share_out_room: int
    avg_price: float
    oneday_avg_price: float
    value: int
    market_price: float
    market_value: int
    gain_loss_value: int
    gl: str
    gain_loss_per: str
    gain_loss_oneday_value: int
    gain_loss_oneday_per: str
    relized: int
    temp_day_out: int
    count: int
    dividend_qty: int
    tax_flag: int
    ceil_price: float
    floor_price: float
    stockType: str
    mc: str


@dataclass
class CashData:
    cash_balance: int
    debt: int
    cash_avai: int
    withdrawal_cash: int
    withdrawal_ee: int
    withdrawal_cash_real: int
    payment: int
    temp_ee: int
    ap_t0: int
    ap_t1: int
    ap_t2: int
    ar_t0: int
    ar_t1: int
    ar_t2: int
    collateral: int
    sell_unmatch: int
    buy_unmatch: int
    cash_block: int
    sum_ap: int
    withdraw: int
    deposit_fee: int
    tempee_used: int
    tempee_using: int
    assets: int
    cash_advance_avai: int
    avaiColla: int
    cash_inout: int
    cash_temp_day_out: int
    cash_withdrawal_block_fo: int
    cash_temp_fs: int
    cash_advance_without_fs: int
    cash_block_give: int
    cash_block_rev: int
    v_advance_payment_limit: int
    v_advance_payment: int
    v_uttb_withdrawal_limit: int
    v_uttb_withdrawal_limit_real: int
    ee_hedging: int
    mm_link_value: int
    use_mm_link: int
    mm_collateral: int
    mm_in_use: int
    assets_4_Withdraw: int
    cash_in_advance: int
    total_asset: int
    total_payment: int
    total_cash: int
    ee_other_asset: int
    gain_loss_oneday_value: int
    gain_loss_oneday_per: float
    gain_loss_value: int
    gain_loss_per: float
    total_market_value: int
    total_avg_value: int
