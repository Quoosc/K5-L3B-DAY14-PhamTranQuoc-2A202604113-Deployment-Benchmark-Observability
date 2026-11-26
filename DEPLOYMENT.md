# Deployment · Day 14

**Nền tảng dự kiến** Railway với Dockerfile Part 6 và Redis trong cùng project. Railway CLI trên máy báo Unauthorized. URL HTTPS và bằng chứng từ tài khoản cloud đang chờ phiên đăng nhập.

## Cấu hình

- Kết nối fork, đặt Root Directory là /06-lab-complete, dùng Dockerfile trong thư mục đó và đặt Health Check Path là /health. Với CLI, từ gốc repo chạy railway up ./06-lab-complete --path-as-root trên service agent đã link. Sau khi deploy, lấy URL qua railway domain. [Railway CLI](https://docs.railway.com/cli/deploying)
- Repo có [railway.toml](06-lab-complete/railway.toml) theo rubric. Với service Railway mới, đặt builder và probe trong Dashboard hoặc dùng Railway Infrastructure as Code. Config as Code bằng TOML dành cho các service hiện đang dùng cơ chế cũ. [Railway Config as Code](https://docs.railway.com/config-as-code)
- Có thể chọn Render, nhập đường dẫn Blueprint 06-lab-complete/render.yaml. Blueprint dùng cùng Dockerfile, tạo web service và Redis tương thích (Key Value) trong cùng region, và tham chiếu connection string nội bộ. [Blueprint](06-lab-complete/render.yaml) · [Render Blueprint Reference](https://render.com/docs/blueprint-spec)

| Biến | Nguồn và tác dụng |
|---|---|
| PORT | Nền tảng cấp cổng, Dockerfile đọc khi khởi động. |
| ENVIRONMENT | Đặt production để nhận diện môi trường qua /health. |
| AGENT_API_KEY | Secret riêng của deployment. Tạo trên dashboard hoặc dùng generateValue của Blueprint. |
| REDIS_URL | URL Redis nội bộ. Railway có thể tham chiếu biến REDIS_URL của service Redis. Render lấy connectionString. |
| RATE_LIMIT_PER_MINUTE | Đặt 10 request mỗi API key trong cửa sổ 60 giây. |
| MONTHLY_BUDGET_USD | Đặt 10 USD theo tháng UTC cho mock LLM. |

## Test Commands

Đặt BASE bằng domain HTTPS agent và nhập key trong phiên Bash với read -rs AGENT_API_KEY. Kiểm tra khi service agent và Redis đã sẵn sàng.

~~~bash
curl -sS -o /dev/null -w 'GET /health %{http_code}\n' "$BASE/health"
curl -sS -o /dev/null -w 'GET /ready %{http_code}\n' "$BASE/ready"
curl -sS -o /dev/null -w 'POST /ask (thiếu key) %{http_code}\n' "$BASE/ask" \
  -H 'Content-Type: application/json' -d '{"question":"Hello"}'
curl -sS -o /dev/null -w 'POST /ask (đúng key) %{http_code}\n' "$BASE/ask" \
  -H 'Content-Type: application/json' -H "X-API-Key: $AGENT_API_KEY" -d '{"question":"Hello"}'
~~~

| Phép thử | Kỳ vọng | Compose local | Public URL |
|---|---:|---:|---|
| GET /health | 200 | 200 | Chờ deploy |
| GET /ready | 200 | 200 | Chờ deploy |
| POST /ask, thiếu key | 401 | 401 | Chờ deploy |
| POST /ask, key đúng | 200 | 200 | Chờ deploy |

## Ảnh deploy

Chờ deployment để thu dashboard.png (đúng service), running.png (service hoạt động và có domain) và test.png (bốn mã HTTP thực nhận trên URL công khai).
