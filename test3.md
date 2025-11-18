Dưới đây là **bản đặc tả kỹ thuật CHI TIẾT – tiếng Việt – dành riêng cho team Codex phía Frontend**.
Em có thể copy nguyên văn gửi cho họ như một **Frontend Functional Specification v1**.

Anh viết theo format tiêu chuẩn của các dự án SaaS/FinTech để team dev dễ hiểu, dễ estimate, dễ triển khai.

---

# 📘 **ĐẶC TẢ KỸ THUẬT FRONTEND – FIN68 DEMO TRADING & BOT BACKTESTING DASHBOARD**

**Phiên bản: v1**
**Dành cho: Codex Frontend Team**
**Ngôn ngữ: Tiếng Việt**
**Trạng thái: Approved**

---

# 1. **Tổng quan dự án**

Dashboard này là một **giao diện Web** phục vụ:

1. **Xem biểu đồ giá** (TradingView Charting Library)
2. **Giao dịch demo (paper trading)** sử dụng dữ liệu giá của Fin68
3. **Chạy backtest bot** (bot predefined từ backend, không cho user viết code)
4. **Theo dõi thống kê bot và demo trading**
5. **Đa tài sản** (cổ phiếu nhiều ngành)
6. Hỗ trợ **margin**, **fee**, **commission** và các thông số giao dịch cơ bản

Frontend chỉ đóng vai trò:

* Hiển thị UI/UX
* Gọi API backend
* Render chart
* Hiển thị kết quả backtest, thống kê
* Quản lý trạng thái phiên

Toàn bộ logic xử lý giá, khớp lệnh, backtest, dòng tiền… **do backend Fin68 đảm nhiệm**.

---

# 2. **Công nghệ bắt buộc**

Codex team **bắt buộc** sử dụng:

### 2.1. **Framework**

* **React** (bắt buộc)
* TypeScript (khuyến nghị mạnh)
* Zustand hoặc React Query cho state management (hoặc theo đề xuất Codex nếu hợp lý)

### 2.2. **Chart**

* **TradingView Charting Library (TVCL)** – bản Charting Library, không phải widget.
  → Fin68 sẽ cấp key hoặc hướng dẫn.

* Sử dụng **custom datafeed** kết nối tới API Fin68.

### 2.3. **Real-time**

* WebSocket để nhận giá theo thời gian thực.
* Tự động reconnect khi mất kết nối.

### 2.4. **UI Framework**

* Có thể dùng MUI, Mantine, Tailwind hoặc bộ UI riêng tùy Codex đề xuất.
* Yêu cầu tổng thể:

  * Dashboard style fintech
  * Dark mode ưu tiên
  * Layout dạng grid / panel chia khu vực

---

# 3. **Cấu trúc tổng thể màn hình**

Dashboard chia thành 3 khối lớn:

---

## **3.1. Header (Top Bar)**

### Thành phần:

1. **Logo Fin68 & tên dự án**:

   * “FIN68 Demo Trading Terminal”

2. **Thanh tìm kiếm mã cổ phiếu**:

   * Autocomplete theo:

     * Ticker
     * Tên công ty
   * Dữ liệu lấy từ API:

     ```
     GET /symbols/search?q=...
     ```
   * Khi user chọn mã → update chart + order ticket.

3. **Bộ lọc ngành / sector**:

   * Dropdown:

     * Tất cả
     * Ngân hàng
     * BĐS
     * Thép
     * Dầu khí
       … (danh sách từ API)
   * Khi chọn → cập nhật danh sách gợi ý trong search.

4. **Tài khoản Demo**

   * Dropdown chọn tài khoản:

     * Demo Account #1
     * Demo Account #2
   * Hiển thị:

     * Equity
     * Margin available

5. **Toggle chế độ**

   * Nút chuyển:

     * **Manual Trading**
     * **Bot Backtesting**

6. **Date Range preset**

   * `YTD`, `1Y`, `6M`, `3M`, `1M`, `Custom`

7. **User Menu**

   * Avatar
   * Settings
   * Logout

---

## **3.2. Khu vực trái – TradingView Chart + Order Ticket**

### **3.2.1. TradingView Chart**

Sử dụng TradingView Charting Library.

#### Yêu cầu:

* Khung biểu đồ bao gồm:

  * Candlestick
  * Volume pane phía dưới
* Hỗ trợ timeframe:

  * `1m`, `5m`, `15m`, `1H`, `1D`
* Loại chart:

  * Candles
  * OHLC
  * Line
* Indicator:

  * SMA
  * EMA
  * RSI
  * MACD
  * Bollinger Bands
* Drawing tools (Phase 1 – tối thiểu):

  * Trendline
  * Horizontal
  * Rectangle

#### Datafeed:

Codex cần implement 1 class datafeed cắm vào TVCL:

* Lấy dữ liệu nến qua API:

  ```
  GET /market/candles?symbol=HPG&tf=1m&start=...&end=...
  ```
* Lấy realtime qua WebSocket:

  ```
  /ws/price?symbol=HPG
  ```

---

### **3.2.2. Order Ticket – Giao dịch demo**

Vị trí: dưới chart hoặc panel slide-in bên phải.

#### Trường dữ liệu:

* **Symbol**: auto fill theo chart
* **Side**: Buy / Sell
* **Order Type**:

  * Market
  * Limit
* **Price** (nếu Limit)
* **Quantity**
* **Margin Leverage**: hiển thị (nhận từ backend)
* **Estimated commission**
* **Estimated margin used**

#### Button:

* **Place Order**
  → Gọi API:

  ```
  POST /demo/orders
  ```

#### Validations:

* Không đủ margin
* Quantity invalid
* Price invalid

---

## **3.3. Khu vực phải – Bot & Statistics Panel**

Gồm 3 tab:

---

### **3.3.1. Tab 1 – Bots (Cấu hình & chạy Backtest)**

#### Gồm 2 phần:

### A. Danh sách bot

* Danh sách bot predefined từ API:

  ```
  GET /bots
  ```
* Mỗi bot hiển thị:

  * Tên
  * Mô tả
  * Tags
  * Universe hỗ trợ (VD: VN30, All Stocks)

### B. Form cấu hình bot

Các trường chung:

* Symbols / Universe (multi-select)
* Timeframe
* Start Date – End Date
* Initial Capital
* Leverage
* Commission rate
* Margin fee
* Slippage (fixed bps hoặc fixed price offset)
* Bot parameters (theo từng bot, trả về từ API)

**Nút Run Backtest**
→ gọi:

```
POST /bots/{bot_id}/backtest
```

Backend trả về:

```
{
  "run_id": "BT20251101_001"
}
```

Chuyển người dùng sang tab “Bot Runs”.

---

### **3.3.2. Tab 2 – Bot Runs (Danh sách + kết quả)**

Bảng dữ liệu:

| Cột             | Ý nghĩa                  |
| --------------- | ------------------------ |
| Run ID          | Mã phiên backtest        |
| Bot Name        | Tên bot                  |
| Symbols         | Mã/Universe              |
| Timeframe       |                          |
| Period          |                          |
| Initial Capital |                          |
| Final Equity    |                          |
| Net Return %    |                          |
| Max Drawdown %  |                          |
| Sharpe Ratio    |                          |
| Status          | running/completed/failed |
| Created At      |                          |

Click vào 1 dòng → mở **Run Detail View** gồm:

#### A. Equity Curve chart

#### B. Drawdown chart

#### C. Bảng Key Metrics:

* CAGR
* Max Drawdown
* Sharpe
* Sortino
* Volatility
* Win rate
* Profit factor
* Avg win / avg loss
* Exposure
* Turnover

#### D. Trade List Table:

* Entry time / price
* Exit time / price
* PnL
* Qty
* Holding period

API:

```
GET /bots/runs
GET /bots/runs/{run_id}
```

---

### **3.3.3. Tab 3 – Bot Metrics (Tổng hợp & so sánh)**

Gồm:

#### 1. Leaderboard

* Top 5 bot theo:

  * Net Return
  * Max DD thấp nhất
  * Sharpe cao nhất

#### 2. Risk-Return Scatter Chart

* X-axis: Max Drawdown
* Y-axis: CAGR hoặc Sharpe
* Mỗi điểm = 1 bot run

#### 3. Bộ lọc:

* Theo timeframe
* Theo sector/universe
* Theo bot

---

# 3.4. Bottom Panel – Positions / Orders / History / Bot Logs

### **Tab 1: Positions**

Columns:

* Symbol
* Side
* Quantity
* Avg Entry
* Last Price
* Market Value
* Unrealized PnL
* Margin Used
* Opened At

### **Tab 2: Open Orders**

Columns:

* Order ID
* Symbol
* Side
* Type
* Price
* Qty
* Filled Qty
* Status
* Created At
* Cancel Button

### **Tab 3: Trade History**

Columns:

* Trade ID
* Symbol
* Side
* Qty
* Entry Price
* Exit Price
* Net PnL
* Fees
* Source (Manual / Bot)
* Entry Time
* Exit Time

### **Tab 4: Bot Trade Log**

Columns:

* Run ID
* Bot Name
* Symbol
* Side
* Qty
* Entry Time
* Exit Time
* Net PnL
* Holding Period

---

# 4. **Các yêu cầu UI/UX**

* Giao diện dạng dashboard 3 panel:

  * Header trên
  * Chart + Order panel bên trái
  * Bot panel bên phải
  * Tabs phía dưới
* Dark mode ưu tiên
* Tốc độ tải chart phải nhanh (<1–2 giây)
* WebSocket tự reconnect
* Loading state rõ ràng khi chạy backtest
* Error state rõ:

  * Lỗi WebSocket
  * Lỗi không đủ margin
  * Lỗi backend khi chạy bot

---

# 5. **Non-functional Requirements**

* Mượt, không lag khi update realtime
* Responsive (desktop-first, tablet-friendly)
* Code phải modular, dễ mở rộng
* Frontend không xử lý nghiệp vụ backtest/trading
* Logs gửi về Fin68 khi cần (optional)
* Tất cả API cài đặt theo dạng Async/Await

---

# 6. **Công việc Codex cần thực hiện**

### **6.1. Frontend Core**

* Build layout dashboard
* Tích hợp TradingView Chart
* Build datafeed cho TVCL
* Xây dựng các tab quản lý:

  * Bots
  * Bot Runs
  * Bot Metrics
  * Positions
  * Orders
  * History
  * Bot Logs
* Order Ticket logic
* State management (React Query, Zustand…)

### **6.2. API Integration**

* Viết hooks/clients:

  * `/market/candles`
  * `/ws/price`
  * `/demo/*`
  * `/bots/*`

### **6.3. UI Components**

* Dropdowns
* Date pickers
* Tables với sort/filter
* Tabs
* Dialogs
* Charts (trừ TradingView)

---

# 7. **Giao diện cần demo cho Fin68**

Codex cần demo các phần sau:

1. Nhúng TradingView + update realtime
2. Đặt lệnh demo + hiển thị lệnh
3. Backtest bot + hiển thị kết quả
4. Bảng thống kê bot (metrics)
5. Bảng Positions/Orders/History
6. UI/UX tổng thể theo mockup

---

Nếu em muốn anh có thể viết thêm:

* Sơ đồ luồng end-to-end (flowchart)
* Mockup dạng Figma/Wireframe
* Phiên bản tiếng Anh tương đương
* API Specs chi tiết đi kèm

Chỉ cần bảo là anh làm tiếp luôn ❤️
