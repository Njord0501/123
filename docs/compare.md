# 資料庫方案比較（設計評估，非並行執行結果）

評分規則：1～5 分，分數愈高愈適合此小型 XR CRUD 專題。此為事前預估；實際 Subagent 並行回報需在 OpenCode 執行並附證據。

| 排名 | 方案 | 建置簡易 | CRUD | 擴充性 | 成本便利 | 合計 /20 | 判斷 |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | SQLite | 5 | 5 | 2 | 5 | 17 | 無需額外伺服器，適合單機作業 |
| 2 | PostgreSQL | 3 | 5 | 5 | 3 | 16 | 多人高併發時更適合 |
| 3 | MongoDB | 3 | 4 | 4 | 3 | 14 | 文件模型靈活，但增加部署與操作負擔 |

## 統一 JSON 範例（預估評分）
```json
[
  {"database":"SQLite","setup_score":5,"crud_score":5,"scale_score":2,"cost_score":5,"total_score":17},
  {"database":"PostgreSQL","setup_score":3,"crud_score":5,"scale_score":5,"cost_score":3,"total_score":16},
  {"database":"MongoDB","setup_score":3,"crud_score":4,"scale_score":4,"cost_score":3,"total_score":14}
]
```

## 選擇理由
本作業規模小、資料結構固定，SQLite 無需啟動獨立資料庫服務，可降低環境配置與測試成本。若未來需要多使用者、複雜查詢或高併發，優先考慮 PostgreSQL。

## 真正並行操作的主 Agent Prompt
請同時啟動 sqlite-eval、postgresql-eval、mongodb-eval 三個子代理，按相同四項指標各自輸出 JSON。收齊後檢查 JSON 欄位與加總正確性，依 total_score 由高到低整理 docs/compare.md，保留理由，不要把預估分數當成實測效能。請提供三個子 session 以便截圖。
