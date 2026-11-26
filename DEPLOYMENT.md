# Deployment · Day 14

**Public URL** [https://day14-agent-ev4m.onrender.com](https://day14-agent-ev4m.onrender.com)

Render triển khai commit `3c77175` của nhánh `main` qua Blueprint `day14-cp6`. Web service Docker `day14-agent` và Key Value (Valkey 8, tương thích Redis) `day14-redis` chạy tại Singapore trên gói Free. Sau thời gian không có traffic, request đầu có thể chờ service khởi động lại.

## Cấu hình

Render đọc [Blueprint Part 6](06-lab-complete/render.yaml), build từ Dockerfile trong `06-lab-complete/`, kiểm tra `/health` và cấp connection string nội bộ cho agent.

| Biến | Nguồn và tác dụng |
|---|---|
| PORT | Nền tảng cấp cổng, Dockerfile đọc khi khởi động. |
| ENVIRONMENT | Đặt production để nhận diện môi trường qua /health. |
| AGENT_API_KEY | Secret riêng của deployment. Render sinh bằng generateValue của Blueprint. |
| REDIS_URL | Render lấy connectionString nội bộ của day14-redis. |
| RATE_LIMIT_PER_MINUTE | Đặt 10 request mỗi API key trong cửa sổ 60 giây. |
| MONTHLY_BUDGET_USD | Đặt 10 USD theo tháng UTC cho mock LLM. |

## Test Commands

Đặt BASE bằng domain HTTPS agent và nhập key trong phiên Bash với read -rs AGENT_API_KEY. Kiểm tra khi service agent và Redis đã sẵn sàng.

~~~bash
BASE=https://day14-agent-ev4m.onrender.com
curl -sS -o /dev/null -w 'GET /health %{http_code}\n' "$BASE/health"
curl -sS -o /dev/null -w 'GET /ready %{http_code}\n' "$BASE/ready"
curl -sS -o /dev/null -w 'POST /ask (thiếu key) %{http_code}\n' "$BASE/ask" \
  -H 'Content-Type: application/json' -d '{"question":"Hello"}'
curl -sS -o /dev/null -w 'POST /ask (đúng key) %{http_code}\n' "$BASE/ask" \
  -H 'Content-Type: application/json' -H "X-API-Key: $AGENT_API_KEY" -d '{"question":"Hello"}'
~~~

| Phép thử | Kỳ vọng | Compose local | Public URL |
|---|---:|---:|---|
| GET /health | 200 | 200 | 200 |
| GET /ready | 200 | 200 | 200 |
| POST /ask, thiếu key | 401 | 401 | 401 |
| POST /ask, key đúng | 200 | 200 | 200 |

## Ảnh deploy

Đo trực tiếp lúc 15:43:26 ngày 26/11/2026 (GMT+7). Ảnh kết quả hiển thị đầu ra của bốn request HTTPS.

- [Dashboard của agent và Redis](screenshots/dashboard.png)
- [Agent Live và domain public](screenshots/running.png)
- [Bốn mã HTTP thực nhận](screenshots/test.png)
