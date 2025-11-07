{
  "meta_context": {
    "version": "1.1.0",
    "dataset": {
      "as_of": {
        "format": "YYYY-MM-DD",
        "description": "Ngày dữ liệu; dùng chung cho toàn payload"
      },
      "market": {
        "codes": {
          "VN": "HOSE+HNX+UPCOM"
        },
        "description": "Mã phạm vi thị trường"
      }
    },

    "conventions": {
      "sign_convention": "Âm = bán ròng, Dương = mua ròng (áp dụng cho mọi net_value_billion)",
      "ranking_rule": "Sắp xếp theo |net_value_billion| giảm dần",
      "missing_data_policy": "Cho phép mảng rỗng khi không có nhóm đáng kể",
      "units": {
        "net_value_billion": "tỷ VND"
      },
      "serialization": {
        "decimal_separator": ".",
        "formats": {
          "net_value_billion": "{:.1f}",
          "share": "{:.2f}",
          "index": "{:.3f}"
        },
        "rounding": "round half up"
      },
      "tone": "Trung lập, định lượng, chuyên nghiệp; không suy đoán nguyên nhân"
    },

    "enums": {
      "dir": [
        "net_buy",
        "net_sell",
        "neutral"
      ],
      "magnitude_bucket": [
        "strongly_negative",
        "negative",
        "neutral",
        "positive",
        "strongly_positive"
      ],
      "breadth_bucket": [
        "bearish",
        "slightly_bearish",
        "neutral",
        "slightly_bullish",
        "bullish"
      ]
    },

    "bucket_rules": {
      "magnitude_bucket": {
        "description": "Cường độ giao dịch ròng cấp NGÀNH/CỔ PHIẾU",
        "hints": {
          "strongly_negative": "Bán ròng rất mạnh",
          "negative": "Bán ròng",
          "neutral": "Cân bằng",
          "positive": "Mua ròng",
          "strongly_positive": "Mua ròng rất mạnh"
        }
      },
      "foreign_breadth_bucket": {
        "by_count_and_value": {
          "breadth_index": "(count_buy - count_sell) / (count_buy + count_sell) ∈ [-1, 1]",
          "value_breadth_index": "buy_value_share - sell_value_share ∈ [-1, 1]"
        },
        "thresholds": [
          { "label": "bearish", "range": "x ≤ -0.50" },
          { "label": "slightly_bearish", "range": "-0.50 < x ≤ -0.20" },
          { "label": "neutral", "range": "-0.20 < x < 0.20" },
          { "label": "slightly_bullish", "range": "0.20 ≤ x < 0.50" },
          { "label": "bullish", "range": "x ≥ 0.50" }
        ],
        "tie_breaker": "Nếu breadth_index và value_breadth_index khác bucket: ưu tiên value_breadth_index; nếu hòa, chọn mức gần 'neutral'.",
        "labels": {
          "bullish": "Lan tỏa MUA RÒNG rất mạnh; phần lớn NGÀNH được mua ròng cả về SỐ LƯỢNG và GIÁ TRỊ.",
          "slightly_bullish": "Nghiêng MUA; số ngành mua ròng nhỉnh hơn, giá trị tập trung phía mua.",
          "neutral": "Cân bằng; số ngành mua/bán và giá trị hai phía tương đương.",
          "slightly_bearish": "Nghiêng BÁN; số ngành bán ròng nhỉnh hơn, giá trị tập trung phía bán.",
          "bearish": "Lan tỏa BÁN RÒNG rất mạnh; phần lớn NGÀNH bị bán ròng cả về SỐ LƯỢNG và GIÁ TRỊ."
        }
      }
    },

    "templates": {
      "sector_item": {
        "icb_code": "Mã ngành chuẩn (ICB của chuẩn nội bộ)",
        "sector_name": "Tên ngành hiển thị",
        "net_value_billion": "Giá trị ròng của ngành (đơn vị: tỷ VND; âm=bán ròng)",
        "dir": "Hướng ròng của ngành trong ngày (enum: dir)",
        "magnitude_bucket": "Cường độ ròng theo thang 5 mức (enum: magnitude_bucket)",
        "top_stocks": "Mảng tối đa 5 phần tử dạng templates.stock_item, sắp theo |net_value_billion| giảm dần"
      },
      "stock_item": {
        "symbol": "Mã cổ phiếu",
        "name": "Tên doanh nghiệp (tuỳ chọn)",
        "net_value_billion": "Giá trị ròng của cổ phiếu (tỷ VND; âm=bán ròng, dương=mua ròng)",
        "rank": "Thứ hạng theo cường độ tuyệt đối trong nhóm"
      },
      "top_group_fields": {
        "description": "Nhóm top theo hướng mua/bán ròng",
        "items": "Mảng 'sector_item' tối đa 3 phần tử; có thể rỗng theo missing_data_policy"
      },
      "foreign_breadth": {
        "scope": "Theo NGÀNH (ICB của chuẩn nội bộ)",
        "count_buy": "Số ngành có net_value_billion > 0",
        "count_sell": "Số ngành có net_value_billion < 0",
        "breadth_index": "Chỉ số độ rộng theo SỐ NGÀNH ∈ [-1,1]; total_sectors=0 ⇒ 0",
        "breadth_bucket": "Bucket định tính 5 mức dựa trên breadth_index & quy tắc tie-break",
        "buy_value_share": "Tỷ trọng giá trị tuyệt đối bên MUA trong [0,1]",
        "sell_value_share": "Tỷ trọng giá trị tuyệt đối bên BÁN trong [0,1]; tổng ≈ 1",
        "value_breadth_bucket": "Bucket theo GIÁ TRỊ; ưu tiên dùng khi không đồng nhất với breadth_bucket",
        "edge_cases": {
          "all_zero": "Nếu mọi ngành có net_value_billion=0 ⇒ breadth_index=0; buy/sell value share = 0; bucket='neutral'",
          "single_side_only": "Nếu chỉ có mua hoặc chỉ có bán ⇒ breadth_index=±1.0; value_breadth_bucket tương ứng"
        }
      }
    },

    "display_guidelines": {
      "summary_snippets": [
        "Net = {net_value_billion_total:.1f} tỷ → {dir_total}; magnitude = {magnitude_bucket_total}",
        "Breadth (by sector): buy/sell = {count_buy}/{count_sell}; value_share buy/sell = {buy_value_share:.2f}/{sell_value_share:.2f} → {breadth_bucket}/{value_breadth_bucket}"
      ],
      "phrase_style": "Ưu tiên 1–2 tính từ ngắn gọn: 'lan tỏa tiêu cực', 'nghiêng bán', 'cân bằng'..."
    },

    "ref_usage": {
      "how_to_reduce_repetition": [
        "Trong payload chính, có thể bỏ trường 'description' nếu nội dung trùng hoàn toàn với templates/enums/conventions ở meta_context.",
        "Các nhóm top_buy_sectors/top_sell_sectors dùng cấu trúc templates.top_group_fields; mỗi phần tử dùng templates.sector_item; nested top_stocks dùng templates.stock_item.",
        "Các nhãn dir/magnitude_bucket/breadth_bucket chỉ cần value/label theo enum."
      ]
    }
  }
}
