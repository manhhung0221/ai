from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from manage_engine import engine_stockDB
Base = declarative_base()
engine = engine_stockDB
class SourceReport(Base):
    __tablename__ = "source_report"
    __table_args__ = {"schema": "info_market"}

    source_id = Column(Integer, primary_key=True, autoincrement=True)
    short_name = Column(String(32), nullable=False, unique=True)
    name = Column(String(255), nullable=False)

    # One-to-many: Một source có nhiều report
    reports = relationship("Report", back_populates="source")

class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "info_market"}

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)

    # One-to-many: Một category có nhiều report
    reports = relationship("Report", back_populates="category")

class Report(Base):
    __tablename__ = "report"
    __table_args__ = {"schema": "info_market"}

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("info_market.categories.category_id"), nullable=False, index=True)
    source_id = Column(Integer, ForeignKey("info_market.source_report.source_id"), nullable=False, index=True)
    source_name = Column(String(64), nullable=False)
    sector_id = Column(Integer, nullable=True, index=True)
    symbol = Column(String(16), nullable=True, index=True)
    title = Column(String(512), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    pages = Column(Integer, nullable=True)
    size = Column(Integer, nullable=True)  # Kích thước file (byte)
    file_name = Column(String(255), nullable=False)
    file_extension = Column(String(16), nullable=False)
    language = Column(String(16), nullable=True)
    downloads = Column(Integer, default=0)
    is_hot = Column(Boolean, default=False)
    id = Column(Integer, autoincrement=True)
    # Many-to-one: Nhiều report thuộc về một category
    category = relationship("Category", back_populates="reports")

    # Many-to-one: Nhiều report thuộc về một source_report
    source = relationship("SourceReport", back_populates="reports")
# Tạo bảng nếu chưa có
Base.metadata.create_all(engine)