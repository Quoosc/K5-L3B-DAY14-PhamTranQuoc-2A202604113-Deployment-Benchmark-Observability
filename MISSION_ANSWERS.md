# Day 14 Lab — Mission Answers

## CP0 · Môi trường

Origin trỏ đến fork đúng mẫu K5-L3B. Kiểm tra GitHub API không xác thực trả HTTP 200. Docker Desktop 4.53.0 (Linux engine trên WSL2), Docker Engine 29.0.1, Compose 2.40.3 và hello-world chạy thành công. Python local 3.11.9 dùng cho các phép đo develop. Các phép thử SIGTERM và checker đầy đủ chạy bằng Python 3.11 trong container Linux trên WSL2, vì máy chỉ có distro docker-desktop.

## Part 1 · Localhost vs Production

### 1.1 · Vấn đề trong develop

| Vị trí | Hành vi | Hậu quả |
|---|---|---|
| [app.py dòng 17](01-localhost-vs-production/develop/app.py#L17) | API key mẫu được gán trực tiếp. | Nếu thay bằng key thật, Git và bản build cũng chứa credential. |
| [app.py dòng 33–38](01-localhost-vs-production/develop/app.py#L33) | In câu hỏi, câu trả lời và key. | PII và secret có thể bị chuyển vào hệ thống thu log. |
| [app.py dòng 21–22](01-localhost-vs-production/develop/app.py#L21) | DEBUG và MAX_TOKENS cố định. | Muốn đổi môi trường phải sửa source. |
| [app.py dòng 51–53](01-localhost-vs-production/develop/app.py#L51) | Bind localhost, port 8000 và bật reload. | Process không nhận kết nối bên ngoài container, port có thể lệch nền tảng, và reload có thể ngắt request khi file đổi. |
| [app.py dòng 42–45](01-localhost-vs-production/develop/app.py#L42) | Thiếu health và readiness. | Platform thiếu tín hiệu riêng cho restart và điều hướng traffic. |
| [app.py dòng 47–54](01-localhost-vs-production/develop/app.py#L47) | App chưa khai báo lifespan để đóng tài nguyên. | Không có bước cleanup riêng của app để xả tài nguyên khi dừng. |

Ví dụ, develop gán key ở app.py:17. Production đọc biến cùng tên bằng os.getenv ở [config.py:27](01-localhost-vs-production/production/config.py#L27). Develop bind localhost ở app.py:51. Production dùng settings.host ở [app.py:196](01-localhost-vs-production/production/app.py#L196) với mặc định 0.0.0.0.

### 1.2–1.3 · Kiểm tra thật

- Develop: từ thư mục develop chạy python -m uvicorn app:app --port 8000, tắt reloader cho lần đo lặp lại trên Windows. POST /ask?question=Hello trả HTTP 200 với answer “Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận.”
- Production: từ thư mục production chạy python app.py với ENVIRONMENT=staging. GET /health trả 200, status=ok, environment=staging. GET /ready trả 200 với {"ready":true}. POST /ask với JSON {"question":"Hello"} trả 200, có question, answer và model=gpt-4o-mini (mock).

| Tính năng | Develop | Production | Tác động khi vận hành |
|---|---|---|---|
| Config và secret | Key, DEBUG, host và port viết trực tiếp | Env qua Settings với kiểm tra lúc nạp | Cùng bản build dùng được với từng môi trường |
| Health | Thiếu probe | /health và /ready | Tách tình trạng process khỏi khả năng nhận traffic |
| Logging | print cả key và payload | logging và JSON cho các sự kiện request | Lọc và phân tích theo trường sự kiện |
| Shutdown | Dựa hoàn toàn vào tiến trình server | Lifespan có bước cleanup | Nơi đóng tài nguyên sau khi server xử lý các request đang chạy |

## Part 2 · Docker

### 2.1 · Dockerfile

1. Base image là python:3.11, bản Python đầy đủ.
2. WORKDIR /app đặt thư mục cho RUN, COPY đường dẫn tương đối và lệnh lúc start.
3. COPY requirements và RUN pip trước source giúp giữ nguyên layer cài thư viện khi chỉ sửa app.py.
4. CMD ["python", "app.py"] là lệnh mặc định. Nếu có ENTRYPOINT dạng exec, CMD cung cấp đối số mặc định cho ENTRYPOINT. Với image này không có ENTRYPOINT riêng, truyền lệnh sau tên image để ghi đè CMD.

### 2.2–2.3 · Build, chạy và đo

Từ gốc repo, chạy `docker build -f 02-docker/develop/Dockerfile -t my-agent:develop .` và `docker build -f 02-docker/production/Dockerfile -t my-agent:advanced .`. Chạy develop với publish 18001:8000 để tránh trùng cổng các phép thử khác. POST /ask?question=Docker trả 200 với answer “Container là cách đóng gói app để chạy ở mọi nơi. Build once, run anywhere!”. docker exec ... python --version trả 3.11.18.

| Tag | Content size, MB thập phân | Disk usage hiển thị |
|---|---:|---:|
| my-agent:develop | 426.32 MB | 1.67 GB |
| my-agent:advanced | 57.41 MB | 240 MB |

docker image inspect --format '{{.Size}}' trả 426320069 và 57409257 byte. Mức giảm theo cùng thước đo content size là (426.320069 − 57.409257) / 426.320069 × 100 = **86.53%**. Stage builder có gcc/libpq-dev và cài requirements. Stage runtime dùng Python slim, chép thư viện đã cài và source cần chạy. Các layer apt và build tools dừng ở builder.

### 2.4 · Compose

~~~text
Client → localhost:80 (Nginx) → agent:8000
                                 ├── Redis:6379     (state/cache)
                                 └── Qdrant:6333    (vector store)
~~~

Các service chung network internal. Agent đợi Redis và Qdrant đạt healthcheck. Nginx phụ thuộc agent và chuyển tiếp HTTP vào agent. Lệnh docker compose -p k5-day14-docker up -d --build đưa cả bốn service lên. Qua Nginx, GET /health trả 200 với status=ok, version=2.0.0. POST /ask {"question":"Explain microservices"} trả 200 với answer “Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.” docker logs phục vụ kiểm tra lỗi khởi động. docker exec chạy kiểm tra phụ thuộc hoặc phiên bản từ bên trong container.

## Part 3 · Cloud Deployment

### 3.1 · Agent Part 6

Agent Part 6 đã deploy lên Render cùng Redis. Kiểm tra qua HTTPS ngày 26/11/2026: GET /health → 200, GET /ready → 200, POST /ask thiếu key → 401, đúng key → 200. [Agent public](https://day14-agent-ev4m.onrender.com) · [Lệnh kiểm tra và ba ảnh deploy](DEPLOYMENT.md).

### 3.2 · So sánh hai mẫu

| Nội dung | [Railway](03-cloud-deployment/railway/railway.toml) | [Render](03-cloud-deployment/render/render.yaml) |
|---|---|---|
| Build/start | Mẫu chọn Nixpacks, start Uvicorn với PORT được cấp | Blueprint Python chạy pip install rồi start Uvicorn theo PORT |
| Probe | /health, timeout 30 s | /health qua healthCheckPath |
| Restart | ON_FAILURE, tối đa 3 lần theo file mẫu | Mẫu giao chính sách restart cho nền tảng, bật autoDeploy khi push |
| Redis | Tạo service riêng trong project | Mẫu khai báo agent-cache trong Blueprint |
| Secret | Đặt qua dashboard hoặc CLI | sync: false để nhập thủ công, generateValue tạo key riêng |

Railway cần nối biến giữa hai service. Render gom service và datastore vào cùng Blueprint. Phần 6 dùng Dockerfile để cả hai nền tảng có cùng môi trường runtime. Với service mới, xem hướng dẫn config trong báo cáo deploy.

### 3.3 · Cloud Run

1. cloudbuild.yaml dùng Python 3.11 cài requirements và chạy pytest. Để bước này thực sự chặn khi pytest fail, shell cần set -e hoặc nối lệnh với && vì mẫu còn echo sau pytest.
2. Docker build gắn tag COMMIT_SHA và latest, rồi push cả hai lên registry.
3. gcloud run deploy trỏ theo COMMIT_SHA, giúp truy vết revision của commit.
4. service.yaml là cấu hình runtime tham chiếu: port 8000, 1 CPU, 512 MiB, Secret Manager, liveness /health, startup /ready, concurrency 80 và 1–10 instance. File mẫu này dùng tag latest, còn pipeline dùng SHA.

## Part 4 · API Gateway

### 4.1 · API key

Gọi POST /ask với body {"question":"Hello"} ở develop và cùng một local key qua biến môi trường. Ba lần gọi lần lượt trả:

~~~text
401  {"detail":"Missing API key. Include header: X-API-Key: <your-key>"}
200  {"question":"Hello","answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic."}
403  {"detail":"Invalid API key."}
~~~

verify_api_key đọc header và đối chiếu AGENT_API_KEY. Để đổi key, đặt env mới rồi khởi động lại app.

### 4.2–4.3 · JWT và rate limit

Ở production, POST /auth/token với tài khoản demo trả **200**, token_type=bearer, expires_in_minutes=60. Gửi Authorization: Bearer bằng biến shell. Server xác thực tài khoản, ký JWT chứa role và thời điểm hết hạn, rồi kiểm tra chữ ký và hạn dùng trước khi xử lý /ask.

Bằng chứng từ lần kiểm lại trên localhost bằng `curl -i`. Request đầu gọi develop khi thiếu key. Hai response tiếp theo lấy từ vòng 20 POST trên production bằng cùng JWT của student. Vòng lặp nhận 10 response 200 và 10 response 429.

~~~text
HTTP/1.1 401 Unauthorized
date: Thu, 26 Nov 2026 08:27:54 GMT
server: uvicorn
content-length: 67
content-type: application/json

{"detail":"Missing API key. Include header: X-API-Key: <your-key>"}

HTTP/1.1 200 OK
date: Thu, 26 Nov 2026 08:27:56 GMT
server: uvicorn
content-length: 186
content-type: application/json
x-content-type-options: nosniff
x-frame-options: DENY
x-xss-protection: 1; mode=block
referrer-policy: strict-origin-when-cross-origin

{"question":"Hello","answer":"Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận.","usage":{"requests_remaining":9,"budget_remaining_usd":1.8e-05}}

HTTP/1.1 429 Too Many Requests
date: Thu, 26 Nov 2026 08:27:57 GMT
server: uvicorn
x-ratelimit-limit: 10
x-ratelimit-remaining: 0
x-ratelimit-reset: 1795681738
retry-after: 59
content-length: 98
content-type: application/json
x-content-type-options: nosniff
x-frame-options: DENY
x-xss-protection: 1; mode=block
referrer-policy: strict-origin-when-cross-origin

{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":59}}
~~~

Cửa sổ trượt 60 giây theo username loại các lần gọi đã hết hạn trước khi đếm. Server chọn giới hạn từ role trong JWT đã xác minh: user 10 req/min và admin 100 req/min.

### 4.4 · Cost guard

Handler mock ước tính token bằng hai lần số từ. Chi phí là (input/1000 × 0.00015) + (output/1000 × 0.0006) USD. Handler kiểm ngân sách trước khi gọi mock, ghi token và chi phí sau khi có kết quả. Mẫu dùng RAM, có giới hạn 1 USD/ngày/user trả 402 và giới hạn 10 USD/ngày/toàn hệ thống trả 503. Trường budget_remaining_usd của /ask mẫu thực tế đang xuất tổng đã dùng. /me/usage mới tính phần dư.

Thiết kế bài tập tháng dùng Redis theo user và kỳ UTC, hết hạn khi sang tháng, và trả 402 nếu dự trù request mới vượt 10 USD. Rate limit kiểm soát lưu lượng theo thời gian ngắn, còn cost guard kiểm soát chi phí tích luỹ dù mỗi phút đều gọi hợp lệ.

## Part 5 · Scaling & Reliability

### 5.1–5.2 · Probes và SIGTERM

Trong develop, dùng python app.py trên Linux. GET /health trả 200, status=ok và memory.used_percent=20.5. GET /ready trả 200, ready=true. Cờ _is_ready được bật sau startup và tắt khi shutdown. Liveness fail có thể khiến orchestrator restart. Readiness fail khiến load balancer tạm ngừng gửi request vào instance.

~~~text
SIGTERM sent
INFO:     Shutting down
INFO:     127.0.0.1:39408 - "POST /ask?question=Long HTTP/1.1" 200 OK
INFO:     Waiting for application shutdown.
2026-11-26 07:54:56,510 INFO 🔄 Graceful shutdown initiated...
2026-11-26 07:54:56,510 INFO ✅ Shutdown complete
INFO:     Application shutdown complete.
EXIT 0
~~~

Request đã bắt đầu tiếp tục nhận 200 sau SIGTERM. Uvicorn dừng nhận kết nối, drain request, gọi lifespan shutdown và thoát.

### 5.3–5.5 · 3 replica và history

docker compose -p k5-day14-scaling up -d --scale agent=3 --wait có đủ ba agent healthy. Dùng override tạm publish 18080 để tránh cổng 8080 của Part 7. Chạy test_stateless.py với cùng logic và đổi riêng BASE_URL trong bản tạm.

~~~text
Session ID: 602a7734-1a9e-4687-90c3-8c1d154db6b9
Request 1: [instance-e0013e]
Request 2: [instance-f970f0]
Request 3: [instance-e54da9]
Request 4: [instance-e0013e]
Request 5: [instance-f970f0]
Total requests: 5
Instances used: {'instance-f970f0', 'instance-e54da9', 'instance-e0013e'}
Total messages: 10
~~~

Nginx chia POST /chat giữa ba replica. Mỗi replica ghi cặp user/assistant theo session ID trong Redis. GET /chat/{session_id}/history đọc 10 message của cùng session trên state chung.

## Part 6 · Production readiness

Chạy python check_production_ready.py nguyên bản trong Linux trên WSL2 với Docker Engine và Redis tạm, không dùng cờ bỏ qua. Image đo 63 MB theo checker. Docker stop mất 0.5 s và trả exit code 0. Checker xác nhận sau hết 5 lượt được cấu hình, request tiếp theo trả 429 và restart agent vẫn trả 429. Ngân sách 0.000001 USD trả 402 ngay lần đầu. Khi Redis mất, /health giữ 200 và /ready trả 503. Test SIGTERM chuyển tiếp cho Uvicorn, request đang xử lý còn 200 và tiến trình thoát 0.

Phép thử riêng với 2 worker, 16 POST đồng thời, rate limit 1000 và ngân sách 0.00004 USD trả 3 mã 200 và 13 mã 402. Redis ghi nhận 30.150 nanodollar, bằng tổng chi phí tính lại từ ba câu trả lời.

Compose agent+Redis qua port thử 18000 với ENVIRONMENT=staging trả health/ready 200, thiếu key 401, đúng key 200. Với key hợp lệ, body thiếu question, câu rỗng, giá trị số và chuỗi chỉ có dấu cách đều trả 422 với chi tiết validation, không có stack trace trong response.

~~~json
{"ts":"2026-11-26T08:00:20.036810+00:00","event":"request","route":"/ask","status":200,"ms":151.78}
{"ts":"2026-11-26T08:00:19.837367+00:00","event":"request","route":"/ask","status":401,"ms":1.01}
~~~

~~~text
  📋 Checklist Deliverable
     ✅ Dockerfile (multi-stage, < 500 MB)
     ✅ docker-compose.yml (agent + redis)
     ✅ .dockerignore
     ✅ Health check endpoint (GET /health)
     ✅ Readiness endpoint (GET /ready)
     ✅ API Key authentication
     ✅ Rate limiting
     ✅ Cost guard
     ✅ Config từ environment variables
     ✅ Structured logging
     ✅ Graceful shutdown
     ✅ Public URL ready (Railway / Render config)
----------------------------------------------------------------
  Result: 12/12 tiêu chí đạt · 43/43 checks passed
  🎉 PASS 12/12 — PRODUCTION READY! Deploy nào!
================================================================
~~~

## Nộp bài trên LMS

LMS ghi nhận lần nộp thứ nhất cho **K5 Lab Day 14 L3B** ngày **26/11/2026**. Trạng thái hiển thị sau khi nộp là **“Your final score is pending”**.

## AI log

Trong các phiên làm việc trên repo, Codex cũng trực tiếp chỉnh sửa code, chạy checker và eval, thu bằng chứng HTTP, triển khai Render và cập nhật báo cáo. Cột cuối ghi phần người học tự khai và kết quả kiểm tra.

| Nội dung hỏi AI | Gợi ý nhận được từ công cụ AI | Phần tôi tự sửa và tự kiểm tra (lệnh & kết quả) |
|---|---|---|
| Rà soát `PLAN_LAB14.md` và các checkpoint Part 1–7 | Gợi ý khung triển khai các module trong `06-lab-complete/app/` (auth, rate_limiter, cost_guard, redis_client, config), multi-stage `Dockerfile`, `docker-compose.yml`, thêm histogram `agent_question_length_chars`, bổ sung kiến thức cho `mock_llm.py` và bố cục trả lời theo rubric. | Tôi trực tiếp đọc đối chiếu từng file cấu hình, chỉnh sửa code và tài liệu KB (`security-02`, `scaling-03`), tự chạy kiểm tra toàn bộ trên máy: build & chạy Docker Compose (`02-docker/production`, `05-scaling-reliability/production`, `06-lab-complete`), chạy `python check_production_ready.py` (kết quả `PASS 12/12`, `43/43 checks passed`), chạy benchmark/eval, Locust, Grafana, Jaeger và Prometheus để lấy số liệu và ảnh chụp thực tế. |
| Đối chiếu rubric và rà soát bằng chứng trước khi nộp | Gợi ý kiểm tra lại cách diễn giải p99 ở `BENCHMARK_REPORT.md` và thêm encoding UTF-8 khi ghi file JSON ở `eval/run_eval.py`. | Tôi tự rà soát lại số liệu đối chiếu với JSON/CSV gốc, sửa diễn giải p99 và cập nhật `run_eval.py`; tự chạy lại API local bằng `curl -i` xác nhận chuỗi mã `401 / 200 / 429` và chạy `python eval/run_eval.py --url http://localhost:8002 --min-accuracy 1.0 --baseline reports/eval_v2.json --out reports/eval_v2_fixed.json` xác nhận `23/23` (`100.00%`), `0 regression`. |
| Triển khai CP6 trên Render | Codex triển khai Blueprint, kiểm tra agent và Redis, thu ảnh Render và kết quả HTTP. | Người học xác nhận triển khai. Codex trực tiếp chạy bốn phép thử HTTPS và ghi nhận 200 / 200 / 401 / 200. |
