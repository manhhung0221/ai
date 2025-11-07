from sqlalchemy import Column, String,FLOAT, TIMESTAMP, Boolean,SmallInteger,ForeignKey,PrimaryKeyConstraint,Integer,Date,Float,DateTime,ForeignKeyConstraint,VARCHAR,func,Text,BigInteger,Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from manage_engine import engine_stockDB
Base = declarative_base()
engine=engine_stockDB

class SymbolInfoTradingView(Base):
    __tablename__ = "symbol_info_tradingview"
    __table_args__ = {"schema": "stock_info"}  # Bạn có thể đổi schema nếu cần

    symbol = Column(String(10), primary_key=True)  # "AAH"
    type = Column(String(20))  # "stock"
    name = Column(String(255))  # "CTCP Hợp Nhất"
    exchange = Column(String(20))  # "UPCOM"
    isListing = Column(Boolean)  # true
    sectorCode = Column(String(10))  # "60"
    industryCode = Column(String(20))  # "601010"
    sector = Column(String(100))  # "Năng lượng"
    industry = Column(String(100))  # "Dầu, khí và than"
    unit = Column(Integer)  # 1
    displayOrder = Column(Integer)  # 0
    session = Column(String(50))  # "0900-1500"
    timezone = Column(String(50))  # "Asia/Ho_Chi_Minh"
    hasIntraday = Column(Boolean)  # true
    hasDaily = Column(Boolean)  # true
    fractionDigits = Column(Integer)  # 2
    sharesOutstanding = Column(FLOAT)  # 117900000
    totalShares = Column(FLOAT)  # 117900000
    icbCode = Column(String(20))  # "60101040"

class SymbolInfo_FA(Base):
    __tablename__ = "stock_info_fa"
    __table_args__ = {"schema": "stock_info"}  # Có thể tùy chọn schema theo cấu trúc project của bạn

    symbol = Column(String(20), primary_key=True, nullable=False)
    name = Column(String(255), nullable=True)
    exchange = Column(String(50), nullable=True)
    icb_industry = Column(String(100), nullable=True)
    type = Column(String(50), nullable=True)

class StockInfo(Base):
    __tablename__ = "stock_info"
    __table_args__ = {"schema": "stock_info"}

    organCode = Column(String(20), nullable=True)
    ticker = Column(String(20), primary_key=True, nullable=False)

    comGroupCode = Column(String(20), ForeignKey("stock_info.index_info.comGroupCode"), nullable=True)
    icbCode = Column(String(10), ForeignKey("stock_info.icb_info.icbCode"), nullable=True)

    organTypeCode = Column(String(10), nullable=True)
    comTypeCode = Column(String(10), nullable=True)
    organName = Column(String(300), nullable=True)
    organShortName = Column(String(300), nullable=True)



class CwInfo(Base):
    __tablename__ = "cw_info"
    __table_args__ = {"schema": "stock_info"}  # Chỉ định schema cụ thể

    coveredWarrantCode = Column(String(20), primary_key=True, nullable=False)
    coveredWarrantName = Column(String(300), nullable=True)
    issuerOrganCode = Column(String(20), nullable=True)
    issuerTicker = Column(String(20), nullable=True)
    derivativeTypeCode = Column(String(10), nullable=True)
    organCode = Column(String(20), nullable=True)
    issuePrice = Column(FLOAT, nullable=True)
    exercisePrice = Column(FLOAT, nullable=True)
    executionRateCoveredWarrant = Column(FLOAT, nullable=True)
    executionRateShare = Column(FLOAT, nullable=True)
    issueDate = Column(TIMESTAMP, nullable=True)
    termStageCode = Column(String(10), nullable=True)
    lastTradingDate = Column(TIMESTAMP, nullable=True)
    maturityDate = Column(TIMESTAMP, nullable=True)
    tradingStatusCode = Column(String(10), nullable=True)
    rightStyleCode = Column(String(10), nullable=True)
    payoutMethodCode = Column(String(20), nullable=True)
    status = Column(Boolean, nullable=True)
    ticker = Column(String(20), nullable=True)
    shareIssue = Column(FLOAT, nullable=True)
    guaranteeValue = Column(FLOAT, nullable=True)
    isinCode = Column(String(100), nullable=True)
    listingDate = Column(TIMESTAMP, nullable=True)
    comGroupCode = Column(String(20), nullable=True)
    derivativeTypeName = Column(String(100), nullable=True)
class IcbInfo(Base):
    __tablename__ = "icb_info"
    __table_args__ = {"schema": "stock_info"}

    icbCode = Column(String(10), primary_key=True, nullable=False)
    icbName = Column(String(300), nullable=True)
    parentIcbCode = Column(String(10), nullable=True)
    friendlyName = Column(String(10), nullable=True)
    icbLevel = Column(SmallInteger, nullable=True)
    icbOrder = Column(SmallInteger, nullable=True)
    sectorProfile = Column(String(20), nullable=True)
    status = Column(SmallInteger, nullable=True)
    createDate = Column(TIMESTAMP, nullable=True)
    updateDate = Column(TIMESTAMP, nullable=True)
    icbCodePath = Column(String(200), nullable=True)
    icbNamePath = Column(String(600), nullable=True)
    industryID = Column(SmallInteger, nullable=True)
    parentIndustryID = Column(SmallInteger, nullable=True)
    icbShortName = Column(String(100), nullable=True)



class IndexInfo(Base):
    __tablename__ = "index_info"
    __table_args__ = {"schema": "stock_info"}

    comGroupCode = Column(String(20), primary_key=True, nullable=False)
    parentComGroupCode = Column(String(20), nullable=True)
    comGroupName = Column(String(20), nullable=True)
    friendlyName = Column(String(20), nullable=True)
    comGroupType = Column(SmallInteger, nullable=True)
    priority = Column(SmallInteger, nullable=True)
    calculateRatio = Column(SmallInteger, nullable=True)
    calculateReturn = Column(SmallInteger, nullable=True)
    priorityIcbIndustry = Column(SmallInteger, nullable=True)
    calculateRatioIcbIndustry = Column(SmallInteger, nullable=True)
    calculateReturnIcbIndustry = Column(SmallInteger, nullable=True)
    comGroupOrder = Column(SmallInteger, nullable=True)
    description = Column(String(200), nullable=True)
    status = Column(SmallInteger, nullable=True)
    createDate = Column(TIMESTAMP, nullable=True)
    updateDate = Column(TIMESTAMP, nullable=True)



class OwnershipStructure(Base):
    __tablename__ = "ownership_structure"
    __table_args__ = {"schema": "stock_info"}  # Chỉ định schema cụ thể

    ticker = Column(String(10), primary_key=True, nullable=False)
    typeOwnership = Column(String(50), primary_key=True, nullable=False)
    percentOwnership = Column(FLOAT, nullable=False)

class ShareholderInfo(Base):
    __tablename__ = "shareholder_info"
    __table_args__ = {"schema": "stock_info"}  # Chỉ định schema cụ thể

    ticker = Column(String(10), primary_key=True, nullable=False)
    shareHolderCode = Column(String(20), primary_key=True, nullable=False)
    shareHolderName = Column(String(300), nullable=False)
    shareHolderType = Column(String(50), nullable=True)
    ownerTypeCode = Column(String(20), nullable=True)
    isFounder = Column(Boolean, nullable=True)
    quantity = Column(FLOAT, nullable=True)
    percentage = Column(FLOAT, nullable=True)
    quantityAdjusted = Column(FLOAT, nullable=True)
    percentageAdjusted = Column(FLOAT, nullable=True)
    publicDate = Column(TIMESTAMP, nullable=True)
class InsiderTrading(Base):
    __tablename__ = "insider_trading"
    __table_args__ = {"schema": "stock_info"}  # Chỉ định schema cụ thể

    ticker = Column(String(10), primary_key=True, nullable=False)
    personId = Column(String(20), primary_key=True, nullable=False)
    fullName = Column(String(100), nullable=False)
    positionName = Column(String(200), nullable=True)
    quantity = Column(FLOAT, nullable=True)
    percentage = Column(FLOAT, nullable=True)
    publicDate = Column(TIMESTAMP, nullable=True)
    isRelationship = Column(Boolean, nullable=True)
class Proxy(Base):
    __tablename__ = "proxy"
    __table_args__ = (
        PrimaryKeyConstraint('ip', 'port'),
        {"schema": "stock_info"}
    )
    ip = Column(String(20), nullable=False)
    port = Column(Integer, nullable=False)
    user = Column(String(20), nullable=True)
    password = Column(String(20), nullable=True)
class CustomKeyMapping(Base):
    """
    ORM model cho bảng lưu trữ custom key mapping.

    Bảng này lưu trữ các mapping giữa key gốc (original_key) và key chuyển đổi (mapped_key),
    giúp dễ dàng truy xuất và bổ sung thông tin mapping trong các ứng dụng.
    """
    __tablename__ = "key_mapping_financial"
    __table_args__ = (
        PrimaryKeyConstraint('original_key','companyType'),
        {"schema": "stock_info"}
    )

    original_key = Column(String(255), nullable=False)
    mapped_key = Column(String(255), nullable=False)
    companyType=Column(String(10), nullable=False)
class Watchlist(Base):
    __tablename__ = "watchlist"
    __table_args__ = {"schema": "stock_info"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    watchListName = Column(String, nullable=True)
    user_id = Column(String, nullable=True)
    displayIndex=Column(Integer,nullable=True)

class WatchlistData(Base):
    __tablename__ = "watchlist_data"
    __table_args__ = {"schema": "stock_info"}

    id = Column(Integer, ForeignKey("stock_info.watchlist.id"), primary_key=True)
    ticker = Column(String, primary_key=True)
    sort_index=Column(Integer,nullable=False)

class Portfolio(Base):
    __tablename__ = "portfolio"
    __table_args__ = {"schema": 'stock_info'}

    user_id   = Column(String(64), primary_key=True, nullable=False)
    port_id   = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    port_name = Column(String(255), nullable=False)
    update_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    moTaNgan       = Column(VARCHAR(50))
    moTaDai        = Column(Text)
    loiNhuanKyVong = Column(VARCHAR(50))
    deposit = Column(BigInteger, nullable=False, server_default="1000000000")
    isPublic = Column(Boolean, nullable=False, server_default='false')
    rebalances = relationship(
        "PortfolioRebalance",
        backref="portfolio",
        cascade="all, delete-orphan",      # Xoá ở ORM, xóa luôn ở database
        passive_deletes=True               # Để ON DELETE CASCADE ở DB phát huy tác dụng
    )
    def __repr__(self):
        return (
            f"<Portfolio(user_id={self.user_id}, port_id={self.port_id}, "
            f"port_name='{self.port_name}', moTaNgan='{self.moTaNgan}', "
            f"loiNhuanKyVong='{self.loiNhuanKyVong}', "
            f"update_at={self.update_at})>"
        )
class PortfolioRebalance(Base):
    __tablename__ = "portfolio_rebalance"
    __table_args__ = {"schema": "stock_info"}

    user_id = Column(String(64), primary_key=True, nullable=False)
    port_id = Column(Integer, primary_key=True, nullable=False)
    ticker  = Column(String(20), primary_key=True, nullable=False)
    Date    = Column(Date, primary_key=True, nullable=False, index=True)
    Weight  = Column(Float, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "port_id"],
            ["stock_info.portfolio.user_id", "stock_info.portfolio.port_id"],
            ondelete="CASCADE"
        ),
        {"schema": "stock_info"}
    )
class NavSeries(Base):
    __tablename__ = "nav_series"
    __table_args__ = {"schema": "stock_info"}

    user_id      = Column(String(64), primary_key=True, nullable=False)
    port_id      = Column(Integer,    primary_key=True, nullable=False)
    date         = Column(Date,       primary_key=True, nullable=False)
    nav_total    = Column(Numeric(20,2), nullable=False)
    nav_stock    = Column(Numeric(20,2), nullable=False)
    cash         = Column(Numeric(20,2), nullable=False)
    nav_by_stock = Column(JSONB, nullable=True)  # JSON hoặc JSONB tự động với PostgreSQL

    def __repr__(self):
        return (f"<NavSeries(user_id={self.user_id}, port_id={self.port_id}, "
                f"date={self.date}, nav_total={self.nav_total}, "
                f"nav_stock={self.nav_stock}, cash={self.cash})>")
class Holder(Base):
    __tablename__ = "holder"
    __table_args__ = (
        PrimaryKeyConstraint("ticker", "majorHolderID", name="pk_holder"),
        {"schema": "stock_info"},
    )

    # Khóa ngoại tham chiếu về StockInfo
    ticker = Column(String(20), ForeignKey("stock_info.stock_info.ticker"), nullable=False)
    majorHolderID = Column(Integer, nullable=False)

    individualHolderID = Column(Integer, nullable=True)
    institutionHolderID = Column(Integer, nullable=True)
    institutionHolderSymbol = Column(String(50), nullable=True)
    institutionHolderExchange = Column(String(50), nullable=True)
    name = Column(String(500), nullable=True)
    position = Column(String(255), nullable=True)

    shares = Column(Float, nullable=True)
    ownership = Column(Float, nullable=True)

    isOrganization = Column(Boolean, nullable=True)
    isForeigner = Column(Boolean, nullable=True)
    isFounder = Column(Boolean, nullable=True)

    reported = Column(DateTime, nullable=True)

    def __repr__(self):
        return (
            f"<Holder(ticker={self.ticker}, majorHolderID={self.majorHolderID}, "
            f"name={self.name}, shares={self.shares}, ownership={self.ownership})>"
        )



Base.metadata.create_all(engine)
SessionLocal = sessionmaker(
    autocommit=False,  # Không tự động commit các thay đổi
    autoflush=False,   # Không tự động gửi các thay đổi trước khi truy vấn
    bind=engine        # Liên kết session với engine cụ thể
)

        
from contextlib import contextmanager
@contextmanager
def get_Info():
    session = SessionLocal()
    try:
        yield session
    finally:
        print("📦 Closing DB session Intra...")
        session.close()