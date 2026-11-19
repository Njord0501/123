# Part A 子代理權限設計

| 角色 | 讀取 | 編輯 | Shell | 說明 |
|---|---|---|---|---|
| architect | 是 | docs/** | 否 | 規格與程式實作分離 |
| coder | 是 | app/** | 否 | 限制程式寫入範圍 |
| tester | 是 | tests/** | 是 | 可執行 pytest，不修改正式程式 |
| reviewer | 是 | 否 | 否 | 獨立唯讀審查 |
| security | 是 | 否 | 否 | OWASP 安全審查加分 |
| doc-writer | 是 | docs/** | 否 | 文件獨立維護 |
| *-eval | 是 | 否 | 否 | 資料庫方案並行比較，唯讀 |

注意：以上使用新版 OpenCode `permission` 語法；老師投影片採用 `permissions` 規則示意。若課堂 OpenCode 版本不同，應依實際版本調整並驗證生效。
