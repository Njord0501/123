# XR Scene Object Management API

依據課堂「使用 Vibe Coding 方法來建立 XR 智慧後端（二）」的作業規格製作。

## 安裝與執行
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API 文件：http://127.0.0.1:8000/docs

## 自動化測試
```bash
python -m pytest -v
```

## POST 範例
```json
{"name":"Cube","model_url":"https://example.com/cube.glb","position":{"x":0,"y":0,"z":0},"rotation":{"x":0,"y":0,"z":0},"scale":{"x":1,"y":1,"z":1}}
```

## 交作業前的必要操作
1. 在 OpenCode 開啟此專案，確認子代理可辨識與權限生效。
2. 請主 Agent 依序指派 team/architect、team/coder，再並行呼叫 team/tester 與 team/reviewer，並呼叫 team/security；必要時請 coder 修正，最多三輪。
3. 請主 Agent 並行呼叫 sqlite-eval、postgresql-eval、mongodb-eval，將實際 JSON 回報替換 docs/compare.md 的預估評分。
4. 記錄單一 Agent 與多子代理的時間及 Token；填寫 docs/reflection_template.md。
5. 截圖主 Agent 派工與至少兩個子 session，提交 GitHub 連結。

注意：本壓縮包提供完整程式、測試與子代理設定，但不代表 OpenCode 子代理已實際運行。未提供憑證驗證、使用者授權與請求限流，不應直接公開部署。
