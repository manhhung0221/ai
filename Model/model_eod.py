from sqlalchemy import create_engine,Column, String, TIMESTAMP,Date, FLOAT, Integer, ForeignKey,BIGINT,NUMERIC,PrimaryKeyConstraint, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from manage_engine import engine_stockDB
Base = declarative_base()
engine = engine_stockDB
class EodStock(Base):
    __tablename__ = "eod_stock_v2"
    __table_args__ = {"schema": "eod"}  # Chỉ định schema

    ticker = Column(String(20), primary_key=True, nullable=False)
    DateTime = Column(TIMESTAMP, nullable=False, primary_key=True)
    Open = Column(FLOAT, nullable=True)
    High = Column(FLOAT, nullable=True)
    Low = Column(FLOAT, nullable=True)
    Close = Column(FLOAT, nullable=True)
    Volume = Column(FLOAT, nullable=True)
    priceAverage = Column(FLOAT, nullable=True)
    priceBasic = Column(FLOAT, nullable=True)
    dealVolume = Column(FLOAT, nullable=True)
    putthroughVolume = Column(FLOAT, nullable=True)
    totalValue = Column(FLOAT, nullable=True) # Tổng giá trị giao dịch
    putthroughValue = Column(FLOAT, nullable=True)
    buyForeignQuantity = Column(FLOAT, nullable=True)
    buyForeignValue = Column(FLOAT, nullable=True)
    sellForeignQuantity = Column(FLOAT, nullable=True)
    sellForeignValue = Column(FLOAT, nullable=True)
    buyCount = Column(FLOAT, nullable=True)
    buyQuantity = Column(FLOAT, nullable=True)
    sellCount = Column(FLOAT, nullable=True)
    sellQuantity = Column(FLOAT, nullable=True)
    adjRatio = Column(FLOAT, nullable=True)
    currentForeignRoom = Column(FLOAT, nullable=True)
    propTradingNetDealValue = Column(FLOAT, nullable=True)
    propTradingNetPTValue = Column(FLOAT, nullable=True)
    propTradingNetValue = Column(FLOAT, nullable=True)
    unit = Column(FLOAT, nullable=True)
    ShareOut = Column(BIGINT, nullable=True)

class StockLastReturns(Base):
    __tablename__ = "stock_last_returns"
    __table_args__ = {"schema": "eod"}

    ticker        = Column(String(20), primary_key=True, nullable=False)
    close_now     = Column(Float, nullable=True)
    close_1w      = Column(Float, nullable=True)
    close_2w      = Column(Float, nullable=True)
    close_1m      = Column(Float, nullable=True)
    close_3m      = Column(Float, nullable=True)
    close_6m      = Column(Float, nullable=True)
    close_1y      = Column(Float, nullable=True)
    datetime_now  = Column(TIMESTAMP, nullable=True)
    last_update   = Column(TIMESTAMP, nullable=True)
class StockTechnicalIndicator(Base):
    __tablename__ = "stock_technical_indicator"
    __table_args__ = {"schema": "eod"}  # hoặc schema nào bạn muốn

    ticker = Column(String, primary_key=True, nullable=False)
    DateTime = Column(Date, primary_key=True, nullable=False)
    indicator = Column(String, primary_key=True, nullable=False)  # ví dụ: 'MA_10', 'RSI_14', ...
    value = Column(Float, nullable=True)
class EodIcb(Base):
    __tablename__ = "eod_icb"
    __table_args__ = {"schema": "eod"}  # Chỉ định schema

    icbCode = Column(String(20), primary_key=True, nullable=False)
    tradingDate = Column(TIMESTAMP, primary_key=True, nullable=False)
    comGroupCode = Column(String(20), nullable=True)
    indexValue = Column(FLOAT, nullable=True)
    indexChange = Column(FLOAT, nullable=True)
    percentIndexChange = Column(FLOAT, nullable=True)
    referenceIndex = Column(FLOAT, nullable=True)
    openIndex = Column(FLOAT, nullable=True)
    closeIndex = Column(FLOAT, nullable=True)
    highestIndex = Column(FLOAT, nullable=True)
    lowestIndex = Column(FLOAT, nullable=True)
    matchVolume = Column(FLOAT, nullable=True)
    matchValue = Column(FLOAT, nullable=True)
    totalMatchVolume = Column(FLOAT, nullable=True)
    totalMatchValue = Column(FLOAT, nullable=True)
class EodInvestorTrades(Base):
    __tablename__ = "eod_investor_trades"
    __table_args__ = {"schema": "eod"}  # Chỉ định schema

    code = Column(String(50), primary_key=True, nullable=False)
    tradingDate = Column(TIMESTAMP, primary_key=True, nullable=False)
    referenceValue = Column(FLOAT, nullable=True)
    referencePrice = Column(FLOAT, nullable=True)
    referenceDate = Column(TIMESTAMP, nullable=True)
    floorValue = Column(FLOAT, nullable=True)
    ceilingValue = Column(FLOAT, nullable=True)
    openValue = Column(FLOAT, nullable=True)
    closeValue = Column(FLOAT, nullable=True)
    closePrice = Column(FLOAT, nullable=True)
    matchValue = Column(FLOAT, nullable=True)
    valueChange = Column(FLOAT, nullable=True)
    percentValueChange = Column(FLOAT, nullable=True)
    highestValue = Column(FLOAT, nullable=True)
    lowestValue = Column(FLOAT, nullable=True)
    averageValue = Column(FLOAT, nullable=True)
    totalMatchVolume = Column(FLOAT, nullable=True)
    totalMatchValue = Column(FLOAT, nullable=True)
    totalDealVolume = Column(FLOAT, nullable=True)
    totalDealValue = Column(FLOAT, nullable=True)
    totalVolume = Column(FLOAT, nullable=True)
    totalValue = Column(FLOAT, nullable=True)
    foreignBuyValue = Column(FLOAT, nullable=True)
    foreignBuyVolume = Column(FLOAT, nullable=True)
    foreignSellValue = Column(FLOAT, nullable=True)
    foreignSellVolume = Column(FLOAT, nullable=True)
    foreignTotalRoom = Column(FLOAT, nullable=True)
    foreignCurrentRoom = Column(FLOAT, nullable=True)
    parValue = Column(FLOAT, nullable=True)
    issueDate = Column(TIMESTAMP, nullable=True)
    iNav = Column(FLOAT, nullable=True)
    iIndex = Column(FLOAT, nullable=True)
    totalTrade = Column(Integer, nullable=True)
    totalBuyTrade = Column(Integer, nullable=True)
    totalSellTrade = Column(Integer, nullable=True)
    totalBuyTradeVolume = Column(FLOAT, nullable=True)
    totalSellTradeVolume = Column(FLOAT, nullable=True)
    shareIssue = Column(FLOAT, nullable=True)
    foreignerPercentage = Column(FLOAT, nullable=True)
    openInterest = Column(FLOAT, nullable=True)
    foreignBuyVolumeMatched = Column(FLOAT, nullable=True)
    foreignBuyValueMatched = Column(FLOAT, nullable=True)
    foreignSellVolumeMatched = Column(FLOAT, nullable=True)
    foreignSellValueMatched = Column(FLOAT, nullable=True)
    foreignBuyVolumeDeal = Column(FLOAT, nullable=True)
    foreignBuyValueDeal = Column(FLOAT, nullable=True)
    foreignSellVolumeDeal = Column(FLOAT, nullable=True)
    foreignSellValueDeal = Column(FLOAT, nullable=True)
    foreignIndividualBuyTradingMatchValue = Column(FLOAT, nullable=True)
    foreignInstitutionalBuyTradingMatchValue = Column(FLOAT, nullable=True)
    foreignIndividualSellTradingMatchValue = Column(FLOAT, nullable=True)
    foreignInstitutionalSellTradingMatchValue = Column(FLOAT, nullable=True)
    foreignIndividualBuyTradingMatchVolume = Column(FLOAT, nullable=True)
    foreignInstitutionalBuyTradingMatchVolume = Column(FLOAT, nullable=True)
    foreignIndividualSellTradingMatchVolume = Column(FLOAT, nullable=True)
    foreignInstitutionalSellTradingMatchVolume = Column(FLOAT, nullable=True)
    localIndividualBuyValue = Column(FLOAT, nullable=True)
    localIndividualBuyVolume = Column(FLOAT, nullable=True)
    localIndividualSellVolume = Column(FLOAT, nullable=True)
    localIndividualSellValue = Column(FLOAT, nullable=True)
    localInstitutionalBuyVolume = Column(FLOAT, nullable=True)
    localInstitutionalBuyValue = Column(FLOAT, nullable=True)
    localInstitutionalSellVolume = Column(FLOAT, nullable=True)
    localInstitutionalSellValue = Column(FLOAT, nullable=True)
    localIndividualBuyMatchVolume = Column(FLOAT, nullable=True)
    localIndividualBuyMatchValue = Column(FLOAT, nullable=True)
    localIndividualSellMatchVolume = Column(FLOAT, nullable=True)
    localIndividualSellMatchValue = Column(FLOAT, nullable=True)
    localInstitutionalBuyMatchVolume = Column(FLOAT, nullable=True)
    localInstitutionalBuyMatchValue = Column(FLOAT, nullable=True)
    localInstitutionalSellMatchVolume = Column(FLOAT, nullable=True)
    localInstitutionalSellMatchValue = Column(FLOAT, nullable=True)
class EODTDStock(Base):
    __tablename__ = "eod_td_stock"
    __table_args__ = {"schema": "eod"}  # Đảm bảo schema là 'eod'

    ticker = Column(String(20), primary_key=True, nullable=False)
    DateTime = Column(TIMESTAMP, primary_key=True, nullable=False, index=True)  # Có index để tối ưu truy vấn
    BuyVolTD = Column(BIGINT, nullable=True)
    BuyValueTD = Column(NUMERIC(18, 2), nullable=True)
    SellVolTD = Column(BIGINT, nullable=True)
    SellValueTD = Column(NUMERIC(18, 2), nullable=True)
    NetValue_TD = Column(NUMERIC(18, 2), nullable=True)  # Tính toán từ BuyValueTD - SellValueTD
class AggTdByIcbDaily(Base):
    __tablename__ = "agg_td_by_icb_daily"
    __table_args__ = {"schema": "eod"}   # Ví dụ đặt ở schema stat

    icbCode = Column(String(10), primary_key=True, nullable=False)
    DateTime = Column(TIMESTAMP, primary_key=True, nullable=False)
    buy_vol = Column(BIGINT, nullable=True)
    buy_value = Column(NUMERIC(18, 2), nullable=True)
    sell_vol = Column(BIGINT, nullable=True)
    sell_value = Column(NUMERIC(18, 2), nullable=True)
    net_value = Column(NUMERIC(18, 2), nullable=True)
    nStocks = Column(Integer, nullable=True)

class IndexContribution(Base):
    __tablename__ = "index_contribution"
    __table_args__ = (
        PrimaryKeyConstraint("ticker", "DateTime", name="pk_index_contribution"),
        {"schema": "eod"},  # đổi schema nếu muốn
    )
    ticker = Column(String(20), nullable=False)
    DateTime = Column(TIMESTAMP, nullable=False)
    contribution = Column(Float, nullable=False)
    comGroupCode = Column(String(10), nullable=False)
# Tạo bảng nếu chưa có
Base.metadata.create_all(engine)
# Tạo một session factory với các tham số cụ thể
SessionLocal = sessionmaker(
    autocommit=False,  # Không tự động commit các thay đổi
    autoflush=False,   # Không tự động gửi các thay đổi trước khi truy vấn
    bind=engine        # Liên kết session với engine cụ thể
)
from contextlib import contextmanager
@contextmanager
def get_EodStock():
    session = SessionLocal()
    try:
        yield session
    finally:
        print("📦 Closing DB session")
        session.close()