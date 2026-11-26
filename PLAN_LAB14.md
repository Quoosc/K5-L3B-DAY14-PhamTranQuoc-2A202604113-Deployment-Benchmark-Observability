# Kế hoạch hoàn thành Lab 14 · Deployment, Benchmark & Observability

**Kết quả cuối lab · 26/11/2026.** Checker Part 6 đạt 12/12 tiêu chí (43/43 phép kiểm). Agent trên Render trả đúng bốn mã CP6: 200, 200, 401, 200. Eval cuối đạt 23/23 câu với 0 regression. LMS đã ghi nhận lần nộp thứ nhất của lớp L3B và đang chờ điểm. Các mục bên dưới lưu lại kế hoạch thực hành ban đầu. [Kết quả thực hành và nộp LMS](MISSION_ANSWERS.md) · [Bằng chứng deploy](DEPLOYMENT.md) · [Số liệu benchmark](BENCHMARK_REPORT.md)

**Mục tiêu là 120/120 điểm thô, quy đổi thành 100/100.** Trong 4 giờ tại lớp, hoàn thành CP0–CP7. Sau lớp, dành thời gian chạy CP8, kiểm tra bản nộp và gửi link trước **23h59 GMT+7 ngày lab**, trừ khi Lab Coach thông báo mốc khác. Mỗi ô dưới đây chỉ đánh dấu sau khi có bằng chứng từ lần chạy của chính mình.

**Hiện trạng khi lập kế hoạch.** Repo có 119 file được Git theo dõi. Part 1–5 đã có ví dụ để chạy. Part 6 còn các hàm chưa triển khai, Compose chưa có Redis và cấu hình deploy mới là khung. Part 7 đã có hai agent mẫu, bộ 23 câu, chương trình đo, dashboard và alert rules. Ở gốc repo chưa có ba báo cáo, thư mục kết quả hay ảnh nộp. Kế hoạch lấy yêu cầu K5 làm chuẩn khi tài liệu mẫu có hướng dẫn khác. [Checkpoints K5](CHECKPOINTS.md) · [Rubric](RUBRIC.md) · [Quy cách nộp](SUBMISSION.md) · [Luật lab](RULES.md)

## 1. Lịch làm và bằng chứng tính điểm

| Mốc | Thời gian từ lúc bắt đầu | Điểm thô | Bằng chứng để chuyển mốc |
|---|---|---:|---|
| CP0 · Setup | 0:00–0:10 | — | Đúng fork, Python trong WSL2, Docker chạy được |
| CP1 · Part 1 | 0:10–0:30 | 8 | 5+ vấn đề, lần gọi thành công, bảng so sánh có giải thích |
| CP2 · Part 2 | 0:30–1:00 | 8 | 4 câu Dockerfile, test container, số MB và %, sơ đồ cùng test Nginx |
| CP3 · Part 4 | 1:00–1:25 | 8 | Output 401/200/429, JWT, giải thích rate limit và cost guard |
| CP4 · Part 5 | 1:25–1:45 | 8 | Probes, SIGTERM, 3 replica, history cùng session qua nhiều instance |
| Nghỉ | 1:45–1:50 | — | Dừng stack Part 5, trả cổng |
| CP5 · Part 6 local | 1:50–2:50 | 50 | Functional 15 + Docker/cấu hình 10 + Security 15 + Reliability 10, full checker đạt 12/12 |
| CP6 · Part 3 và deploy Part 6 | 2:50–3:15 | 18 | Part 3 được 8, deployment Part 6 được 10. Một URL thật, 4 phép thử, 3 ảnh |
| CP7 · Part 7 local | 3:15–4:00 | 9 | Load/SLO 4 + eval/gate 5. Đủ 10 JSON, eval cuối 23/23 |
| CP8 · Part 7 stack và nộp | Sau lớp, trước hạn | 11 | Observability 4 + tracing 3 + alerts/chaos 4. Đủ 2 CSV, 4 ảnh, báo cáo và link LMS |

Kẹt một mốc quá 10 phút thì ghi lỗi, lệnh và thư mục đang chạy, hỏi Lab Coach rồi làm phần độc lập tiếp theo. Giữ đủ 60 phút cho CP5. Mục 12 của checker xét cấu hình deploy. Điểm deployment còn cần URL và phép thử thực tế ở CP6. Part 6 mở rộng như streaming và history không có điểm bonus. [Hướng dẫn làm bài K5](README.md) · [Tiêu chí con](INSTRUCTOR_GUIDE.md)

### Tra cứu nguồn khi hướng dẫn khác nhau

| Khi cần xác nhận | Nguồn và cách áp dụng cho lớp K5 |
|---|---|
| Điểm và tiêu chí con | Lấy bảng K5 cho Part 3 và Part 6. Đối chiếu từng exercise của Part 1, 2, 4, 5 và từng mục nhỏ Part 7 với hướng dẫn chấm. Tổng thô × 100/120, làm tròn 0,5 điểm. Mốc đạt là 84/120, tương đương 70/100. [Rubric K5](RUBRIC.md) · [Hướng dẫn chấm](INSTRUCTOR_GUIDE.md) |
| Exercise và cách chạy trên máy này | Dùng đề bài tập để xác định câu hỏi cần trả lời. Dùng README và checkpoints K5 cho WSL2, endpoint, cổng, thứ tự deploy và thời điểm lưu bằng chứng. [Đề từng exercise](CODE_LAB.md) · [Lưu ý K5](README.md) · [Các checkpoint](CHECKPOINTS.md) |
| Cây thư mục, báo cáo và hạn nộp | Theo cây thư mục K5 trong submission. Dùng delivery checklist để soát nội dung ba báo cáo và luật lab để kiểm AI log, secret, dữ liệu cá nhân và commit hợp lệ. [Cấu trúc nộp](SUBMISSION.md) · [Delivery checklist](DAY14_DELIVERY_CHECKLIST.md) · [Luật lab](RULES.md) |
| Bằng chứng Part 6–7 | Đối chiếu hành vi ứng dụng với hợp đồng và checker Part 6. Đối chiếu số liệu, ảnh và lời giải thích với đúng mục của template Part 7. [Hợp đồng agent](06-lab-complete/README.md) · [Checker](06-lab-complete/check_production_ready.py) · [Hướng dẫn benchmark](06-lab-complete/benchmark-observability/README.md) · [Mẫu báo cáo](06-lab-complete/benchmark-observability/BENCHMARK_REPORT_TEMPLATE.md) |
| Khi lệnh mẫu gặp lỗi | Tra theo triệu chứng, rồi chạy lại đúng phép thử của checkpoint. [Troubleshooting](TROUBLESHOOTING.md) · [Quick reference](QUICK_REFERENCE.md) |

## 2. CP0–CP4 · Chạy ví dụ và viết MISSION_ANSWERS.md

### CP0 · Chuẩn bị đúng môi trường

- [ ] Kiểm tra `git remote -v` tại gốc repo. `origin` phải là fork cá nhân đúng tên theo mẫu K5-L3B trong `SUBMISSION.md`. Xác nhận repo Public và đối chiếu deadline với LMS/Lab Coach.
- [ ] Trên máy Windows này, mở **WSL2 Bash**, vào thư mục repo trên ổ E (đường dẫn dưới `/mnt/e/`), bật Docker Desktop tích hợp với distro đó. Các khối lệnh sau dùng Bash. Trong mỗi terminal, từ repo chạy `ROOT="$(git rev-parse --show-toplevel)"`. Nếu dùng venv, tạo bằng Python 3.11+ trong WSL, kích hoạt ở cả terminal chạy app và terminal chạy test. Mỗi khi chuyển ví dụ, cài đúng `python -m pip install -r requirements.txt` tại thư mục chứa app.

```bash
python --version
python -c "import os; print(os.name)"   # phải là posix để test SIGTERM
docker compose version
docker run --rm hello-world
```

- [ ] Tạo `MISSION_ANSWERS.md` ở gốc với các mục Part 1–5, mục output Part 6 và **AI log** ở cuối. Tạo sẵn thư mục ảnh bằng `mkdir -p "$ROOT/screenshots"`. Với mỗi exercise, ghi thư mục/lệnh → kết quả thật đã che secret → kết luận và lý do. Khi dùng AI cho code Part 6 hoặc câu trả lời, ghi câu hỏi, gợi ý nhận được, phần mình sửa và phép thử mình tự thực hiện. Có thể ghi lần đọc repo/lập kế hoạch này nếu dùng nó để soạn bài.
- [ ] Các ví dụ dùng chung cổng 8000. Dừng process/container cũ trước khi đổi app. Dùng tên Compose riêng trong mọi lệnh của mỗi phần, kể cả khi xem log và dọn stack. Với Part 2 và 5, tạo `.env.local` trống ở đúng thư mục `production/`.

### CP1 · Part 1, Exercise 1.1–1.3 (2 + 2 + 4)

1. **1.1** Đọc `01-localhost-vs-production/develop/app.py`. Ghi ít nhất 5 vấn đề cụ thể, mỗi vấn đề có vị trí và hậu quả. Có thể xét secret trong mã/log, cấu hình cố định, bind host, cổng, debug/reload, thiếu probes hoặc xử lý shutdown. Dẫn ít nhất một cặp dòng develop/production thể hiện thay đổi, che giá trị secret.
2. **1.2** Trong `develop/`, cài dependencies, chạy `python app.py`. Ở terminal khác gọi `curl -i -X POST 'http://localhost:8000/ask?question=Hello'`. Lưu status và trường trả lời. Bản này đọc query parameter.
3. **1.3** Dừng develop. Trong `production/`, tạo `.env` local từ `.env.example`, đặt biến cần dùng trong môi trường, cài requirements rồi chạy app. Kiểm tra `/health`, `/ready` và `POST /ask` bằng JSON. Trong **Part 1** lập bảng **Tính năng | Develop | Production | Tác động khi vận hành**, tối thiểu có config/secret, health, logging, shutdown.

### CP2 · Part 2, Exercise 2.1–2.4 (mỗi bài 2 điểm)

1. **2.1** Trả lời 4 câu theo `02-docker/develop/Dockerfile`: base image/tag, `WORKDIR`, lý do copy requirements trước source để tận dụng cache, và cách `CMD` tương tác với `ENTRYPOINT`. Hai demo Go ở `layer-order/` và `multi-stages/` minh họa phần giải thích.
2. **2.2–2.3** Build từ **gốc repo** vì đường dẫn `COPY` bắt đầu từ gốc. Chạy develop, gọi endpoint qua query như CP1, giữ output rồi dừng container. Lưu bảng `docker images` có hai tag. Ghi số MB cùng đơn vị và tính **% giảm = (develop − advanced) / develop × 100**. Giải thích phần nào được cài ở builder, phần nào được chép sang runtime và vì sao kích thước thực tế khác nhau.

```bash
cd "$ROOT"
docker build -f 02-docker/develop/Dockerfile -t my-agent:develop .
docker build -f 02-docker/production/Dockerfile -t my-agent:advanced .
docker images my-agent
docker run --rm -p 8000:8000 my-agent:develop
# Terminal khác
curl -i -X POST 'http://localhost:8000/ask?question=Docker'
```

3. **2.4** Trong `02-docker/production/`, chạy `touch .env.local`, rồi `docker compose -p k5-day14-docker up -d --build`. Kiểm tra `ps` với cùng `-p`. Trong **Part 2**, vẽ sơ đồ client → Nginx cổng 80 → agent:8000, kèm Redis:6379 và Qdrant:6333 trên mạng nội bộ, ghi vai trò từng service và dependencies theo Compose. Lưu kết quả `curl -i http://localhost/health` và `curl -i -X POST http://localhost/ask -H 'Content-Type: application/json' -d '{"question":"Explain microservices"}'`. Dọn stack bằng `docker compose -p k5-day14-docker down`.

### CP3 · Part 4, Exercise 4.1–4.4 (mỗi bài 2 điểm)

1. **4.1** Trong `04-api-gateway/develop/`, chạy app với `AGENT_API_KEY` dành riêng cho demo local. Gọi `POST /ask` với JSON hợp lệ lần lượt thiếu key, đúng key, sai key. Dán output `curl -i` đã che key. Ví dụ này trả **401 khi thiếu, 200 khi đúng, 403 khi sai**. Chỉ ra dependency `verify_api_key` và cách đổi key qua env rồi khởi động lại.
2. **4.2** Dừng develop, cài requirements và chạy `python app.py` trong `04-api-gateway/production/`. Lấy token của user demo rồi gọi endpoint. Giải thích bước kiểm tra tài khoản → ký JWT có role/thời hạn → xác minh chữ ký và hạn dùng. Dùng biến shell để giữ token ngoài ảnh và báo cáo.

```bash
TOKEN=$(curl -fsS http://localhost:8000/auth/token -H 'Content-Type: application/json' \
  -d '{"username":"student","password":"demo123"}' | python -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')
for i in {1..20}; do
  curl -si http://localhost:8000/ask -H "Authorization: Bearer $TOKEN" \
    -H 'Content-Type: application/json' -d '{"question":"Hello"}'
  echo
done
```

3. **4.3** Giữ một response 200 và một response 429 từ vòng lặp, gồm header/body liên quan. Giải thích sliding window 60 giây theo user trong `rate_limiter.py`, user thường 10 req/min, role admin có hạn mức riêng 100 req/min. Đây là quyết định phân quyền của server.
4. **4.4** Đọc `cost_guard.py`, mô tả số token, cách tính USD, kiểm tra trước khi gọi model và ghi usage sau đó. Phân biệt ví dụ Part 4 dùng RAM với thiết kế Exercise 4.4 dùng Redis theo user/tháng ngân sách 10 USD, reset khi đổi tháng, vượt ngân sách trả 402. Giải thích vì sao cần cả hạn mức tốc độ và hạn mức tiền. Lưu cả bốn exercise dưới **Part 4**.

### CP4 · Part 5, Exercise 5.1–5.5 (2 + 2 + 2 + 1 + 1)

1. **5.1** Chạy `05-scaling-reliability/develop/app.py` trong thư mục của nó. Lưu status/body từ `/health` và `/ready`. Mô tả khi nào platform restart process, khi nào load balancer tạm ngừng gửi traffic, và điều kiện cờ readiness thực sự kiểm ở bản develop.
2. **5.2** Khởi động app bằng `python app.py &`, lưu `APP_PID=$!`, chờ ready. Gọi `curl -i -X POST 'http://localhost:8000/ask?question=Long' &`, gửi `kill -TERM "$APP_PID"` khi request đang xử lý. Lưu response và đoạn log shutdown để giải thích trình tự ngừng nhận → xử lý nốt → giải phóng → thoát. Nếu request chưa tới, chạy lại và xác nhận thời điểm từ log.
3. **5.3–5.5** Trong `05-scaling-reliability/production/`, thực hiện các lệnh dưới đây. Dùng session ID, tập `served_by` và `count` thực tế để giải thích vì sao history vẫn đầy đủ sau 5 câu ngay cả khi đổi instance. Liên hệ với `POST /chat`, `GET /chat/{session_id}/history` và state chung trong Redis. Script tự gửi câu hỏi và đọc history. Thí nghiệm đó không tự tắt replica.

```bash
touch .env.local
docker compose -p k5-day14-scaling up -d --build --scale agent=3
docker compose -p k5-day14-scaling ps
python test_stateless.py                  # dùng http://localhost:8080
docker compose -p k5-day14-scaling logs agent --tail=30
docker compose -p k5-day14-scaling down
```

**Hoàn thành CP4** khi **Part 5** có hai probe, kết quả request giữa lúc SIGTERM, vai trò của Redis/Nginx và output chứng minh nhiều instance dùng chung history. Nếu chỉ thấy một `served_by`, kiểm tra lại ba container và log trước khi kết luận. Khi debug container ở CP2 hoặc CP4, dùng `docker logs <tên-container>` để xem lỗi khởi động và `docker exec <tên-container> <lệnh>` để kiểm tra từ bên trong container theo câu hỏi cuối Part 2.

## 3. CP5 · Hoàn thiện agent Part 6 trong 06-lab-complete/

Từ `06-lab-complete/`, cài requirements, chạy `python check_production_ready.py --static-only` để thấy hiện trạng. Mỗi hàng dưới ứng với **một mục của checker**. Sửa trực tiếp bản khung, giữ entry point `app.main:app`, dùng mock LLM có sẵn và giữ nguyên script chấm. [Hợp đồng Part 6](06-lab-complete/README.md) · [Script chấm](06-lab-complete/check_production_ready.py)

| Thứ tự làm | Mục checker | Việc cần triển khai và phép thử |
|---:|---|---|
| 1 | 4 · Health | Trong `app/main.py`, tạo `GET /health`. Khi process sống, nhận 200 cả khi khởi động mà Redis chưa sẵn sàng. |
| 2 | 9 · Environment | Trong `app/config.py`, đọc và ép kiểu `PORT`, `ENVIRONMENT`, `AGENT_API_KEY`, `REDIS_URL`, `RATE_LIMIT_PER_MINUTE`, biến ngân sách. Chọn `MONTHLY_BUDGET_USD` mặc định 10 để khớp checklist tháng, hoặc hỗ trợ thêm ngân sách ngày nếu dùng. Lập `.env.example` đầy đủ với giá trị mẫu an toàn. Thử ghi đè bằng env trong staging. |
| 3 | 10 · Structured logging | Mỗi dòng log ứng dụng là một JSON object hợp lệ. Ghi event, status, thời gian xử lý. Thử parse một dòng thành công và một dòng lỗi. Loại key/token khỏi nội dung log. |
| 4 | 6 · API key | Trong `app/auth.py`, gắn dependency đọc `X-API-Key` vào `POST /ask`. Thiếu hoặc sai đều **401** theo rubric Part 6. Key đúng + JSON `{"question":"Hello"}` trả 200 với câu trả lời từ mock. |
| 5 | 5 · Readiness | `app/redis_client.py` tạo client từ `REDIS_URL`, ping có timeout. `/ready` trả 200 khi sẵn sàng, 503 khi Redis mất. Thử cặp `/health` và `/ready` trong cùng sự cố. |
| 6 | 7 · Rate limiting | `app/rate_limiter.py` lưu bộ đếm/cửa sổ 60 giây theo API key trong Redis. Cập nhật nguyên tử giữa workers, đặt TTL. Mặc định 10 req/min, trả 429 cùng `Retry-After` khi vượt. Chạy hai worker, dùng hết lượt, restart **agent** rồi thử lại trong cùng cửa sổ, phải còn bị chặn. |
| 7 | 8 · Cost guard | `app/cost_guard.py` kiểm budget trước LLM, tính tiền từ số token input/output và đơn giá trong file, cộng vào Redis theo kỳ. Mock Part 6 trả chuỗi nên ghi rõ cách ước tính token. Cộng chi phí nguyên tử, dùng cùng trạng thái qua nhiều worker. Thử với ngân sách rất nhỏ và rate limit đủ cao để thấy 402. |
| 8 | 11 · Graceful shutdown | Dùng lifespan đóng tài nguyên sau khi xử lý xong request. Giữ cơ chế nhận SIGTERM của Uvicorn. Test request đang chạy vẫn nhận 200, process thoát sạch, `docker stop` dưới 10 giây và exit code 0. |
| 9 | 1 · Dockerfile | Tách builder và runtime slim, copy dependencies/app/utils cần dùng, chạy non-root, thêm `HEALTHCHECK`. Lệnh khởi động dùng `exec uvicorn` với host `0.0.0.0`, port `${PORT:-8000}`, Uvicorn là PID 1. Build từ `06-lab-complete/`. Xác nhận image < 500 MB và container trả `/health` khi thiếu Redis. |
| 10 | 3 · .dockerignore | Thêm pattern thực cho `.env`, file env local, `__pycache__`, `venv`, `.venv`. Có thể loại `benchmark-observability/` khỏi build context của Part 6. |
| 11 | 2 · Compose | `docker-compose.yml` có service agent build tại đây và service dùng `redis:*`. Agent có `depends_on` và `REDIS_URL` trỏ vào tên service Redis. Kiểm tra cấu hình bằng `docker compose config -q`, bật stack, xác nhận `/ready` 200 và `/ask` hoạt động. |
| 12 | 12 · Deploy config | Chọn Railway thì hoàn thiện `railway.toml` với builder `DOCKERFILE`, `healthcheckPath = "/health"`. Chọn Render thì hoàn thiện `render.yaml` với web service Docker, `healthCheckPath: /health` và secret dùng `generateValue` hoặc `sync: false`. Checker kiểm mọi config có nội dung thực. |

**Đối chiếu 60 điểm Part 6 trước khi chuyển mốc.**

- [x] **Functional 15** — 10 cho `/ask` trả lời đúng, 5 cho lỗi rõ ràng. Thử body thiếu/rỗng/sai kiểu với key hợp lệ, ghi mã 4xx và xác nhận response không lộ stack trace.
- [x] **Docker/cấu hình 10** — multi-stage 4, image < 500 MB 2, Compose agent + Redis 2, cấu hình env 2.
- [x] **Security 15** — cả thiếu/sai key 401 (4), vượt rate 429 với state Redis (4), vượt budget 402 (4), không hardcode secret (3).
- [ ] **Reliability 10** — liveness 2, readiness 2, SIGTERM 3, stateless 3. **Deployment 10** được kiểm tiếp ở CP6 — URL 5, config 3, env trên cloud 2.
- [x] Trên **WSL2 có Docker đang chạy**, dùng Redis dành cho lab hoặc để checker tạo Redis tạm. Chạy lại `python check_production_ready.py` **không có cờ bỏ qua** sau thay đổi cuối. Dán nguyên khối **📋 Checklist Deliverable**, dòng `Result` và `PASS 12/12` vào `MISSION_ANSWERS.md`. Mục ⚠️ cũng là chưa đạt. Nếu lỗi, sửa nguyên nhân và chạy lại bản đầy đủ.

## 4. CP6 · Deploy chính agent Part 6 và viết DEPLOYMENT.md

1. **Chọn một nền tảng chính.** Lộ trình mặc định dùng Railway. Tạo project với hai service agent và Redis. Nếu kết nối từ GitHub, chọn fork cá nhân, đặt Root Directory là `06-lab-complete/` và trỏ config đúng thư mục. Nếu dùng CLI theo hướng dẫn K5, liên kết đúng project/service, chạy `railway up` từ `06-lab-complete/`, rồi lấy domain bằng `railway domain`. Trong cả hai trường hợp, xác nhận build log đang dùng Dockerfile Python của Part 6. Dockerfile ở gốc repo là ví dụ Go. Phương án Render dùng Blueprint `06-lab-complete/render.yaml`, khai báo web service cùng Redis và kiểm tra Docker context. Theo quy định lớp, dùng gói miễn phí/dùng thử và liên hệ Lab Coach nếu nền tảng yêu cầu thẻ mà bạn không muốn nhập.
2. **Đặt env ở service agent.** Đặt key riêng của deployment, `REDIS_URL` nội bộ của Redis cloud, môi trường, rate limit, budget và các biến app thực sự dùng. App phải lắng nghe `PORT` do nền tảng cấp. Ghi tên biến, mục đích và nguồn cấp vào `DEPLOYMENT.md`. Che giá trị secret, URI có mật khẩu và token. Kiểm tra deployment logs, lấy URL HTTPS public và giữ service hoạt động đến khi chấm xong.
3. **Chạy 4 phép thử public.** Đặt `BASE` là URL thật (bỏ dấu / cuối), nhập key vào biến shell bằng `read -rs AGENT_API_KEY`. Tắt shell tracing nếu đang bật. Ghi **cả lệnh lẫn mã thực nhận** dưới mục Test Commands của `DEPLOYMENT.md`.

```bash
curl -sS -o /dev/null -w 'GET /health  %{http_code}\n' "$BASE/health"
curl -sS -o /dev/null -w 'GET /ready   %{http_code}\n' "$BASE/ready"
curl -sS -o /dev/null -w 'POST /ask (thiếu key) %{http_code}\n' "$BASE/ask" \
  -H 'Content-Type: application/json' -d '{"question":"Hello"}'
curl -sS -o /dev/null -w 'POST /ask (đúng key)  %{http_code}\n' "$BASE/ask" \
  -H 'Content-Type: application/json' -H "X-API-Key: $AGENT_API_KEY" -d '{"question":"Hello"}'
```

4. **Chốt Part 6 và Part 3.** Chuỗi kỳ vọng **200 / 200 / 401 / 200**. `--public-url` của checker chỉ kiểm thêm `/health`. Lưu `screenshots/dashboard.png` (deployment dashboard đúng service), `running.png` (service đang chạy, có URL), `test.png` (4 mã trên public URL). Trong `DEPLOYMENT.md` điền platform, URL bấm được, cách test, env và liên kết cả 3 ảnh. Kiểm tra ảnh mở được, không lộ thông tin tài khoản.
5. **Viết Part 3 trong MISSION_ANSWERS.md.** Ghi URL, nền tảng, kết quả test và link bằng chứng để lấy **4 điểm**. Để lấy **3 điểm** cho nền tảng còn lại, đối chiếu `03-cloud-deployment/railway/railway.toml` và `03-cloud-deployment/render/render.yaml` về build/start, probe, restart, khai báo service Redis và quản lý secret. Giải thích khác biệt tác động thế nào khi triển khai. Với **1 điểm Exercise 3.3**, đọc cả hai YAML ở `03-cloud-deployment/production-cloud-run/`, viết **3–5 dòng** theo pipeline test → build/tag image → push registry → deploy Cloud Run theo SHA. Liên hệ `service.yaml` với cấu hình runtime, probes, secret và scaling. Bài này chỉ yêu cầu đọc cấu hình.

Sau khi đã chụp đủ bốn mã CP6, có thể làm thêm self-test trong delivery checklist trên deployment của mình. Với giới hạn mặc định 10 lần/phút, gửi tối đa 15 POST hợp lệ liên tiếp bằng cùng key, lưu lần đầu thấy 429, rồi chờ cửa sổ hạn mức hết trước khi kiểm lại 200. Trong `DEPLOYMENT.md`, ghi tên các biến thực dùng, kể cả `LOG_LEVEL` nếu app hỗ trợ. Kiểm tra URL từ một thiết bị khác theo gợi ý của BTC.

## 5. CP7 · Benchmark local và thu đủ 10 JSON

Part 7 chạy agent riêng trong `06-lab-complete/benchmark-observability/`. Giữ nguyên auth, rate limit và cost guard của agent Part 6 đã deploy. Ở gốc repo, tạo báo cáo **một lần** rồi dùng cùng file đến cuối CP8.

```bash
cd "$ROOT"
cp -n 06-lab-complete/benchmark-observability/BENCHMARK_REPORT_TEMPLATE.md BENCHMARK_REPORT.md
cd 06-lab-complete/benchmark-observability/develop
python -m pip install -r requirements.txt
mkdir -p reports
```

### 7.1 · Metrics và SLO

- [x] Trong `develop/app.py`, thêm Histogram **`agent_question_length_chars`** với bucket độ dài hữu hạn. Trong handler `/ask` quan sát `len(body.question)` một lần mỗi câu hợp lệ. Từ thư mục `develop/`, mở hai terminal: `AGENT_VERSION=v1 PORT=8001 python app.py` và `AGENT_VERSION=v2 PORT=8002 python app.py`. Kiểm tra `/health` hiển thị version đúng mỗi cổng.
- [x] Gửi `POST /ask` tới 8002 rồi đọc `/metrics`. Trong báo cáo, trích một Counter (`http_requests_total`), Gauge (`agent_in_flight_requests`) và Histogram. Xác nhận `agent_question_length_chars_count` tăng sau request. Giải thích tại sao `route.path`/`unmatched` giữ số lượng chuỗi thời gian hữu hạn, còn URL tùy ý có thể tạo quá nhiều label.
- [x] Điền phần đầu template (họ tên tại ô quy định, ngày chạy, CPU/RAM, Docker/WSL). Trong **§1**, chốt SLI, ngưỡng và lý do **trước khi đo**. Mặc định `load_test.py` xét p95 ≤ 500 ms, error rate ≤ 2%. Ghi rõ accuracy tối thiểu cho CI (85%) và điều kiện nghiệm thu bản fixed (100%, 0 regression).

### 7.2 · Concurrency và tail latency

Chạy các lệnh sau từ `develop/` khi v2 ở cấu hình mặc định. Mỗi lần chỉ chạy một load test. Giữ nguyên model, điều kiện máy và các biến mock ngoài biến đang khảo sát.

```bash
for c in 1 10 50 100; do
  python load_test.py --url http://localhost:8002 --requests 300 --concurrency "$c" \
    --out "reports/load_v2_c${c}.json"
done
```

- [x] **§2.1** Mỗi hàng lấy `rps`, `latency_ms.p50/p95/p99`, `error_rate × 100` và `slo.passed` từ đúng file. Kiểm tra `total_requests=300`. Error rate tính trên mọi request, latency trong script lấy từ HTTP 200. Nếu exit 1 vì vi phạm SLO, giữ report và phân tích hàng FAIL. Tránh `set -e` khi thu loạt phép đo dự kiến có FAIL.
- [x] **§2.2** Lần lượt đặt `s=0`, `s=0.03`, `s=0.1`. Mỗi lần dừng **riêng v2**, bật lại bằng `AGENT_VERSION=v2 PORT=8002 MOCK_SLOW_RATE="$s" python app.py`. Ở terminal đo, đặt cùng `s` rồi chạy lệnh dưới. Sao chép `latency_ms.avg/p95/p99` từ ba file, giải thích sự khác biệt giữa trung bình và nhóm request chậm nhất. Nhận xét RPS có tăng tuyến tính theo concurrency hay không dựa trên số thực đo.

```bash
python load_test.py --url http://localhost:8002 --requests 300 --concurrency 20 \
  --out "reports/load_v2_slow_${s}.json"
```

### 7.3 · Eval trước/sau khi sửa knowledge base và quality gate

1. Trả v2 về slow rate mặc định. Giữ v1/v2 cùng điều kiện để so chất lượng, cost và latency. Ghi mọi override dùng riêng cho eval (nếu đặt `MOCK_ERROR_RATE=0` để cô lập lỗi chất lượng, áp dụng cho cả hai và lần fixed). Lưu hai baseline **trước khi sửa KB**.

```bash
python eval/run_eval.py --url http://localhost:8001 --out reports/eval_v1.json
python eval/run_eval.py --url http://localhost:8002 --baseline reports/eval_v1.json --out reports/eval_v2.json
```

2. Trong `eval_v2.json`, lọc `results[]` có `passed=false`, đọc ID, answer, `missing_keywords` và kiểm tra có lỗi HTTP nào không. Hai ca kiến thức đề nhắm tới là `scaling-03` và `security-02`. Sửa **`develop/utils/mock_llm.py` của Part 7**, bổ sung tài liệu HPA/autoscaling và API key/JWT vào `KNOWLEDGE_BASE` theo lỗi quan sát được. Giữ nguyên bộ câu hỏi, đáp án và ngưỡng chấm từng câu.
3. Tắt/bật lại v2 để nạp KB mới. Chạy lệnh cuối, giữ nguyên tên file hai baseline. Điều kiện hoàn thành là `passed=total=23`, `accuracy=1.0`, `quality_gate.regressions=[]`, `quality_gate.passed=true` và exit code 0.

```bash
python eval/run_eval.py --url http://localhost:8002 --min-accuracy 1.0 \
  --baseline reports/eval_v2.json --out reports/eval_v2_fixed.json
```

4. **§3** Điền 3 cột v1/v2/fixed từ `accuracy`, `avg_tokens`, `total_cost_usd`, `cost_per_correct_usd` và `quality_gate.passed`. So sánh thêm `latency_ms.p95`, giải thích trade-off accuracy, retrieval, số token và chi phí trên mỗi câu đúng. Ghi từng ID sai, keyword thiếu và chỉnh sửa đã khắc phục nó.
5. **CI của 7.3** Lập job PR `.github/workflows/eval.yml` hoặc viết giải thích tương đương vào §3 theo CP7. Job dùng Python 3.11, cài đúng requirements trong `develop/`, bật v2, chờ `/health`, chạy `eval/run_eval.py` với `--min-accuracy 0.85` và `--baseline` trỏ tới report đã duyệt ở gốc repo. Exit 1 khi dưới ngưỡng **hoặc** có ID từng đúng nay sai. Để thực sự chặn merge, dùng job làm required status check. Thử luồng FAIL bằng cách gọi v1 với baseline v2, đọc `echo $?` ngay sau lệnh. Dùng đường dẫn riêng hoặc bỏ `--out` ở phép thử này để bảo toàn baseline.

## 6. CP8 · Observability, tracing, alerts và scaling

Chạy mọi lệnh trong `06-lab-complete/benchmark-observability/production/`. Đặt hàm Bash sau trong từng terminal của CP8 để mọi lệnh đều tác động đến cùng stack. Dùng `.env` local của **stack observability**. Chụp ảnh và lấy log trước khi dọn volume.

```bash
cd "$ROOT/06-lab-complete/benchmark-observability/production"
cp -n .env.example .env
dc() { docker compose -p k5-day14-observability "$@"; }
dc up -d --build --scale agent=1
dc ps
```

### 7.7 · Đo scaling khi cấu hình còn ở baseline

Chạy hai phép đo trước phần gây lỗi để hai CSV so sánh được. Giữ nguyên v2/model/mock rates và dừng tải từ Locust UI trong cả hai lần. Trước mỗi lần đo, chờ DNS cập nhật khoảng 15 giây và xác nhận đúng số target `agent` đang UP ở Prometheus.

```bash
dc run --rm locust -f /mnt/locust/locustfile.py --host http://nginx \
  --headless -u 100 -r 10 -t 2m --csv /mnt/results/scale_1
dc up -d --scale agent=3
# Chờ Prometheus thấy đủ 3 target UP trước khi đo.
dc run --rm locust -f /mnt/locust/locustfile.py --host http://nginx \
  --headless -u 100 -r 10 -t 2m --csv /mnt/results/scale_3
```

Trong **§5**, lấy cùng loại dòng ở hai `*_stats.csv`. Dùng `Aggregated` cho kết quả toàn workload và ghi rõ workload có cả `/ask` và `/health`. Đọc Requests/s, 50%, 95%, 99%, Failure Count và tính tỷ lệ lỗi từ số request nếu thảo luận về error rate. So p95 và RPS của 1/3 instance, đối chiếu panel LLM latency để lý giải nút thắt. Nếu Locust exit 1, đọc bảng failures và xác minh có tải hợp lệ trước khi dùng số. Hàng loạt 401 hoặc lỗi kết nối là lý do sửa môi trường và đo lại.

### 7.4 · Dashboard dưới tải

- [x] Chuyển sang `dc up -d --scale agent=2` cho câu hỏi chia tải. Kiểm tra hai target ở `localhost:9090/targets`. Bật Locust UI `localhost:8089`, host `http://nginx`, **30 users, ramp-up 5 users/s**. Khi dashboard đã có dữ liệu, mở Grafana `localhost:3000` → **Day 14 — AI Agent Overview**, chọn khoảng thời gian có tải.
- [x] Chụp `screenshots/grafana-dashboard.png`. Trong **§4.1**, ghi thời điểm/cửa sổ, đọc traffic, error rate, latency, saturation (in-flight). Trả lời đủ bốn câu 7.4: (1) avg và p95 bao nhiêu, khoảng cách nói lên điều gì, (2) req/s của từng replica cho thấy Nginx chia tải thế nào, (3) retrieval/context tác động lên input và output tokens/s ra sao, (4) `curl -i http://localhost:8080/metrics` cho kết quả gì. Nginx cấu hình 404 cho đường dẫn này, còn Prometheus scrape từng agent qua mạng Compose.

### 7.5 · Liên kết Jaeger với log thật

- [x] Mở `localhost:16686`, chọn service `observable-agent` → **Longest First**, mở trace chậm. Chụp `screenshots/jaeger-slow-trace.png` thấy waterfall và span con tốn thời gian nhất. Trong **§4.3**, ghi `trace_id`, tổng ms, tên span, ms và **% = ms span / ms toàn trace × 100**.
- [x] Sao chép ID của **chính trace chậm** vào biến `TRACE_ID`, chạy `dc logs --no-color --no-log-prefix agent | grep -F "$TRACE_ID"`. Dán một dòng JSON ứng dụng có cùng ID vào §4.3. Kiểm tra ID trong ảnh, log và báo cáo khớp từng ký tự.
- [x] Lọc thêm `error=true`, mở span lỗi có event `exception`. Chụp `screenshots/jaeger-error-trace.png`. Nếu chưa có lỗi, thu ảnh trong thí nghiệm A bên dưới. Có thể lấy ID từ log `llm_error` để tìm đúng trace lỗi.

### 7.6 · Tạo hai alert cùng firing và hoàn tất báo cáo

1. Test rule từ thư mục `production/`. Ghi kết quả riêng cho unit test và cho lần quan sát thật trên trang Alerts.

```bash
docker run --rm -v "$PWD/prometheus:/p:ro" -w /p --entrypoint promtool \
  prom/prometheus:v3.16.0 test rules /p/alert_rules_test.yml
```

2. Giữ Locust UI chạy 30 users. Lấy mốc giờ bắt đầu và ở cùng múi giờ cho mọi lần đo. Trong `.env` đặt **A** `MOCK_ERROR_RATE=0.2`, áp dụng `dc up -d --scale agent=2`, ghi thời điểm thay đổi và lần đầu thấy `AgentHighErrorRate` firing. Giữ A, bật thêm **B** `MOCK_SLOW_RATE=0.3` rồi áp dụng lại. Theo dõi `localhost:9090/alerts` đến khi **AgentHighErrorRate và AgentHighLatencyP95 đồng thời firing trên cùng một trang**. Khi container được tạo lại, chờ target mới được scrape và cả hai rule đủ thời gian điều kiện.
3. Chụp **một ảnh** `screenshots/prometheus-alert-firing.png` đọc được tên và trạng thái firing của **hai rule khác nhau**. Trong **§4.2**, ghi thay đổi, alert, mốc bắt đầu, thời điểm firing, thời gian chênh và panel xác nhận. Rule trong repo dùng ngưỡng 5xx > 5% với `for: 1m` và p95 > 1 giây với `for: 2m`. Hai khoảng `for` là cấu hình, thời gian phát hiện trong bảng phải đo trên stack.
4. Để điền đầy đủ bảng A–E, trả về baseline giữa các thí nghiệm tiếp theo. **C** đổi sang `LLM_MODEL=mock-llm-large`, kiểm cost/giờ và `LLMCostBurnRateHigh`. **D** dùng `dc ps` chọn đúng một container agent của lab rồi `docker pause` riêng container đó, theo dõi `up`, `AgentInstanceDown` và lỗi phía Nginx/Locust, sau đó `docker unpause`. **E** đổi `AGENT_VERSION=v1`, quan sát bảng version, retrieval/tokens và đối chiếu eval v1 với v2. Với thay đổi env, áp dụng lại bằng `dc up -d --scale agent=2`. Ghi panel và kết quả thực tế, kể cả khi không firing trong thời gian quan sát. Phân tích vì sao 504 ở proxy có thể vắng trên metric agent và vì sao cần eval định kỳ/gate để phát hiện suy giảm chất lượng ở E.
5. **7.7** Hoàn thiện **§6** bằng 3 điều học được dựa trên số liệu của bài và một đề xuất metric/alert cho production có lý do. Liên kết cả 4 ảnh Part 7 trong báo cáo. Xác nhận đã lấy log, CSV, ảnh, khôi phục env local rồi `dc down -v` khi xong.

Với mỗi thí nghiệm đã chạy ở §4.2, lưu ảnh dashboard và trang Alerts tại thời điểm quan sát. Riêng E, ghi lại trạng thái quan sát được ngay cả khi các rule vẫn inactive. Có thể liên kết ảnh chi tiết bên cạnh từng dòng A–E. Tên của **7 ảnh BTC yêu cầu trong bộ nộp chính** được liệt kê ở mục 7. [Hướng dẫn thí nghiệm, mục 2.6](06-lab-complete/benchmark-observability/README.md) · [Danh mục ảnh nộp](SUBMISSION.md)

**Đối chiếu 20 điểm Part 7 khi đọc lại báo cáo**

| Nhóm | Phân bổ theo hướng dẫn chấm | Nơi tìm bằng chứng |
|---|---|---|
| Load & SLO · 4 | Bảng concurrency đủ chỉ số (2đ), phân tích tail latency ở ba slow rate (2đ) | §2.1–2.2 và 7 JSON load |
| Eval & gate · 5 | So chất lượng/chi phí/latency (2đ), đạt 23/23 và 0 regression (2đ), CI chặn merge (1đ) | §3 và 3 JSON eval |
| Observability · 4 | Dashboard có tải và đọc đúng panel (2đ), trả lời đủ bốn câu 7.4 (2đ) | §4.1 và ảnh Grafana |
| Tracing · 3 | Tìm span chậm nhất và ghi số ms (2đ), đối chiếu log bằng cùng trace ID (1đ) | §4.3, log JSON và ảnh Jaeger |
| Alerts & chaos · 4 | Một ảnh thấy ít nhất hai rule cùng firing và có số đo thời gian phát hiện trong báo cáo (2đ), phân tích E hoặc lỗi 504 (2đ) | §4.2 và ảnh Prometheus |

Bảng scaling §5, hai CSV Locust và phần kết luận §6 phải có trong bộ nộp. [Tiêu chí con Part 7](INSTRUCTOR_GUIDE.md) · [Rubric K5](RUBRIC.md)

## 7. Đóng gói và kiểm tra commit được chấm

Từ gốc repo, chép kết quả của lần đo cuối ra đúng vị trí. Báo cáo đã điền ở gốc từ CP7.

```bash
cd "$ROOT"
mkdir -p reports benchmark-results screenshots
cp 06-lab-complete/benchmark-observability/develop/reports/{load_v2_c{1,10,50,100},load_v2_slow_{0,0.03,0.1},eval_v1,eval_v2,eval_v2_fixed}.json reports/
cp 06-lab-complete/benchmark-observability/production/benchmark-results/scale_{1,3}_stats.csv benchmark-results/
```

| Đường dẫn BTC sẽ mở | Danh mục bắt buộc và điều kiện nghiệm thu |
|---|---|
| `MISSION_ANSWERS.md` | Đủ Part 1–5 theo exercise, output full checker 12/12, AI log cuối file. |
| `DEPLOYMENT.md` | Nền tảng, public URL của agent Part 6, 4 lệnh và mã trả về, tên env và 3 link ảnh deploy. |
| `BENCHMARK_REPORT.md` | Đủ đầu trang và §1–§6 template. Mỗi bảng trỏ được về JSON/CSV/ảnh hoặc log tương ứng, có đơn vị và nhận xét từ kết quả thật. |
| `reports/` · 10 JSON | `load_v2_c1.json`, `load_v2_c10.json`, `load_v2_c50.json`, `load_v2_c100.json`, `load_v2_slow_0.json`, `load_v2_slow_0.03.json`, `load_v2_slow_0.1.json`, `eval_v1.json`, `eval_v2.json`, `eval_v2_fixed.json`. |
| `benchmark-results/` · 2 CSV | `scale_1_stats.csv`, `scale_3_stats.csv`. Mở được cả hai bảng, có số request thực. |
| `screenshots/` · 7 PNG | `dashboard.png`, `running.png`, `test.png`, `grafana-dashboard.png`, `jaeger-slow-trace.png`, `jaeger-error-trace.png`, `prometheus-alert-firing.png`. |
| `06-lab-complete/` | App và cấu hình Part 6 đúng đường dẫn checker. README có thể dùng để tái chạy với cấu hình đã chọn. Part 7 có histogram mới và KB develop đã sửa. |

**Kiểm lần cuối trước khi gửi link LMS**

- [ ] So tên fork với mẫu `K5-L3B-DAY14-HoVaTen-MSSV-Deployment-Benchmark-Observability`. Họ tên viết liền, không dấu, viết hoa chữ đầu mỗi thành tố. Kiểm lịch sử commit có thông điệp rõ, và thử tái chạy theo `06-lab-complete/README.md` với config đang nộp. Tự giải thích được một đoạn xử lý trong `app/` và truy ngược được một số bất kỳ trong benchmark về bằng chứng gốc.
- [ ] Kiểm các trường hợp mất điểm trước khi push. Secret thật hoặc `.env` từng vào lịch sử Git bị trừ 10 điểm. Sai tên repo/vị trí file bị trừ 5 nếu vẫn tìm được bài. Repo private không mở được hoặc không tìm được bài sẽ không được chấm. Số không khớp JSON/CSV làm mất toàn bộ điểm mục Part 7 tương ứng. Sửa checker để lấy PASS làm Part 6 bị 0. Sao chép làm cả hai bài mất điểm phần liên quan. Trường hợp cần nộp muộn phải có sự đồng ý trước của Lab Coach theo luật lab. [Rubric và mức trừ](RUBRIC.md) · [Luật lab](RULES.md)
- [ ] Chạy full checker trên code cuối. Kiểm lại 4 lệnh public ở CP6, mở từng ảnh qua link trong báo cáo và đối chiếu số liệu theo file gốc. Chỉ đánh dấu PASS cho kết quả đã chạy. Số đo/SLO FAIL có bằng chứng vẫn là kết quả cần báo cáo.
- [ ] Qua `git status --short` và `git diff --cached`, kiểm tra danh mục đã stage, chọn đúng file để commit. Giữ nguyên `06-lab-complete/check_production_ready.py` và `06-lab-complete/benchmark-observability/develop/eval/golden_dataset.jsonl` so với đề. Chỉ nộp file mẫu `.env.example`, không commit key, token, URI có mật khẩu hoặc file env local. Kiểm `git log --all --oneline -- '*.env' '.env'` theo BTC và rà các tên như `.env.local`, nội dung Markdown, source, ảnh cùng lịch sử commit. Nếu từng lộ secret thật, thu hồi/đổi key ngay và báo Lab Coach.
- [ ] Bài cá nhân dùng URL, ảnh và số đo của chính mình. Không để email/số điện thoại trong bài. Họ tên và MSSV chỉ đặt ở vị trí BTC cho phép. Nếu có thay đổi luật/bài mẫu từ trước khi làm, kiểm diff riêng trước khi chọn nội dung commit.
- [ ] Push lên fork đúng tên và **Public**. Mở link ở cửa sổ ẩn danh, kiểm tra commit cuối, 3 báo cáo, 10 JSON, 2 CSV, 7 ảnh và source Part 6 **trên GitHub**. Gửi **một link repo** trên LMS trước hạn, kiểm tra LMS đã ghi nhận. Bản chấm là commit cuối trước deadline. Không force-push hoặc sửa ngày commit. Giữ service cloud đến sau khi được chấm. [Danh sách tự kiểm của BTC](SUBMISSION.md) · [Mẫu nội dung báo cáo](DAY14_DELIVERY_CHECKLIST.md) · [Mẫu benchmark đủ 6 mục](06-lab-complete/benchmark-observability/BENCHMARK_REPORT_TEMPLATE.md)
