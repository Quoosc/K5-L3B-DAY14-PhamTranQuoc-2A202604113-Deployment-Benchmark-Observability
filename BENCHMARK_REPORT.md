# Benchmark & Observability Report — Day 14

- **Họ tên** Phạm Trần Quốc
- **Ngày chạy** 26/11/2026 (GMT+7)
- **Môi trường** Windows, Python 3.11.9. Intel Core i7-12700H (14 lõi, 20 luồng), 15.69 GiB RAM. Docker Desktop 4.53.0 trên WSL2, Linux engine báo 20 CPU logic và 7.60 GiB RAM.

## 1. SLO của agent

| SLI | SLO | Lý do |
|---|---|---|
| p95 latency /ask | ≤ 500 ms | Giới hạn thời gian chờ của phần lớn request thành công và phát hiện tail latency. |
| Error rate /ask | ≤ 2% | Cho phép tỷ lệ lỗi mock mặc định 1% và phát hiện lần chạy có tỷ lệ lỗi cao hơn. |
| Accuracy trên golden dataset | CI ≥ 85%. Bản fixed 100% và 0 regression | Chặn suy giảm chất lượng theo ngưỡng chung và từng câu từng đúng. |

Sau một POST /ask hợp lệ, agent_question_length_chars_count tăng từ 0.0 lên 1.0. Counter http_requests_total{method="POST",route="/ask",status="200"} bằng 1.0. Gauge agent_in_flight_requests bằng 0.0 sau khi request hoàn thành. Histogram agent_question_length_chars_bucket{le="16.0"} bằng 1.0. Histogram dùng các ngưỡng 16–2000 ký tự. Label route lấy mẫu route đã khai báo hoặc unmatched, giúp giữ số chuỗi hữu hạn khi client gửi nhiều URL lạ.

## 2. Benchmark hiệu năng (develop)

### 2.1 · Concurrency vs latency

300 request mỗi lần, agent v2 fixed, mock-llm-small và mock rates mặc định. Tỷ lệ lỗi dùng toàn bộ request. Các percentile tính từ response HTTP 200.

| Concurrency | RPS | p50 (ms) | p95 (ms) | p99 (ms) | Error rate | SLO |
|---:|---:|---:|---:|---:|---:|:---|
| [1](reports/load_v2_c1.json) | 4.26 | 202.6 | 234.9 | 1718.3 | 0.67% | PASS |
| [10](reports/load_v2_c10.json) | 36.80 | 191.9 | 233.6 | 1704.6 | 1.67% | PASS |
| [50](reports/load_v2_c50.json) | 100.65 | 221.1 | 897.7 | 1978.9 | 0.33% | FAIL |
| [100](reports/load_v2_c100.json) | 41.31 | 1253.2 | 5511.8 | 5680.4 | 1.67% | FAIL |

Concurrency tăng từ 10 đến 50 làm throughput tăng 2.74 lần và p95 vượt ngưỡng. Từ 50 đến 100, throughput giảm từ 100.65 xuống 41.31 req/s và p95 tăng lên 5511.8 ms. Dữ liệu phù hợp với hiện tượng tranh chấp tài nguyên hoặc chờ ở client/server khi mở nhiều kết nối cùng lúc. Phép đo này dùng chung máy cho client và server nên chưa định vị được điểm bão hoà chính xác.

### 2.2 · Tail latency

300 request mỗi lần, concurrency 20, khởi động lại v2 giữa các mức slow rate.

| MOCK_SLOW_RATE | avg (ms) | p95 (ms) | p99 (ms) |
|---|---:|---:|---:|
| [0](reports/load_v2_slow_0.json) | 196.0 | 240.7 | 249.2 |
| [0.03](reports/load_v2_slow_0.03.json) | 225.6 | 236.3 | 1703.1 |
| [0.1](reports/load_v2_slow_0.1.json) | 389.3 | 1689.8 | 1730.2 |

Ở slow rate 3%, p99 tăng gần 7 lần và average tăng khoảng 30 ms. Nhóm chậm rơi vào 1% đuôi, trong khi p95 vẫn thuộc nhóm nhanh. Ở mức 10%, p95 cũng vọt lên khoảng 1.69 s dù average vẫn dưới 0.4 s.

## 3. Benchmark chất lượng (develop)

| Chỉ số | [Agent v1](reports/eval_v1.json) | [Agent v2](reports/eval_v2.json) | [Agent v2 fixed](reports/eval_v2_fixed.json) |
|---|---:|---:|---:|
| Accuracy | 4.35% (1/23) | 91.30% (21/23) | 100.00% (23/23) |
| Avg tokens / câu | 57.5 | 108.7 | 114.9 |
| Tổng cost (USD) | 0.000409 | 0.000756 | 0.000801 |
| Cost / câu đúng (USD) | 0.00040935 | 0.00003599 | 0.00003485 |
| p95 latency (ms) | 191.6 | 247.0 | 237.0 |
| Quality gate theo lần chạy | FAIL | PASS | PASS |
| Lỗi HTTP | 0 | 0 | 0 |

| ID | Keyword thiếu trong v2 | Thay đổi trong KB develop |
|---|---|---|
| security-02 | token, hết hạn, chữ ký | Mục JWT/API key giải thích claims, hạn dùng và kiểm chữ ký. |
| scaling-03 | cpu, memory, custom metrics | Mục HPA giải thích điều chỉnh số replica theo CPU, memory hoặc chỉ số tuỳ chỉnh. |

Cả ba lần đặt MOCK_ERROR_RATE=0 để cô lập chất lượng. Trường dataset trong ba JSON dùng đường dẫn tương đối để bỏ đường dẫn máy local. Số liệu và chi tiết từng câu giữ nguyên. Baseline v1 và v2 dùng ngưỡng mặc định 80%, sau đó fixed chạy với --min-accuracy 1.0 và --baseline reports/eval_v2.json. Fixed chạy exit 0, quality_gate.regressions rỗng. Retrieval tăng số token và thời gian xử lý so với v1, trong khi chi phí mỗi câu đúng giảm nhờ có thêm nhiều câu đúng. Chênh lệch p95 10 ms giữa hai lần eval v2 trên 23 câu có thể do biến thiên mock.

[Workflow Agent eval](.github/workflows/eval.yml) dùng Python 3.11 để bật v2 trên PR và đợi /health. Job áp dụng ngưỡng 85% và ưu tiên report fixed ở commit đích làm baseline. PR đầu tiên dùng baseline v2 được đưa vào cùng repo nếu commit đích chưa có report fixed. Test âm tính với v1 so với baseline v2 tại ngưỡng 85% trả exit 1. Để áp dụng cho merge trên GitHub, cấu hình job Quality gate thành required status check của nhánh đích. Trạng thái branch protection chưa xác minh.

## 4. Observability stack (production)

### 4.1 · Grafana dưới tải

02 replica v2. Locust web chạy 30 users, 5 users/s. Ảnh chụp sau khi ramp-up. Số liệu dưới đây lấy từ các truy vấn của dashboard lúc **14:59:18 GMT+7**, cửa sổ rate 1 phút trừ gauge tức thời. [Ảnh dashboard](screenshots/grafana-dashboard.png)

| Panel | Giá trị |
|---|---:|
| Traffic POST /ask | 17.69 req/s |
| Error rate 5xx | 0.72% |
| Latency avg | 238.0 ms |
| Latency p95 | 294.5 ms |
| Saturation | 6 request in-flight |
| Requests/s theo instance | 172.24.0.7:8000 = 8.87, 172.24.0.8:8000 = 8.82 |
| Tokens/s | Input 1286.5, output 683.8 |
| Retrieval hit ratio (cửa sổ 5 phút) | 88.75% |

1. p95 cao hơn avg 56.5 ms. p99 ở cùng thời điểm là 1852.6 ms, cho thấy một nhóm nhỏ chậm hơn nhiều dù p95 chỉ khoảng 295 ms.
2. Hai replica có 8.87 và 8.82 req/s, gần một nửa tổng lưu lượng cho mỗi replica.
3. Retrieval bổ sung văn bản vào prompt nên input tokens/s cao hơn. Output phụ thuộc câu trả lời được chọn, và khác biệt v1/v2 được kiểm qua panel Tokens/s và thí nghiệm E.
4. GET http://localhost:8080/metrics qua Nginx trả **404**. Prometheus đọc /metrics trực tiếp trên từng agent qua network Compose.

### 4.2 · Chaos và thời gian phát hiện

promtool test rules /p/alert_rules_test.yml chạy **SUCCESS** với prom/prometheus:v3.16.0. Kết quả này là unit test của rules. Bảng dưới dùng lần quan sát trên stack thật, theo giờ GMT+7.

| # | Thay đổi | Bắt đầu → lần đầu thấy firing | Panel và kết quả | Ảnh |
|---|---|---|---|---|
| A | MOCK_ERROR_RATE=0.2 | 14:59:23 → 15:00:59, **96 s**, AgentHighErrorRate | Error rate 19.98%. Alert chi phí đã firing trước khi bật A. | [Grafana](screenshots/chaos-A-grafana.png) · [Alerts](screenshots/chaos-A-alerts.png) |
| B | Giữ A, thêm MOCK_SLOW_RATE=0.3 | 15:01:07 → 15:03:44, **157 s**, AgentHighLatencyP95 | p95 1904.9 ms, error rate 18.21%. Cả AgentHighLatencyP95 và AgentHighErrorRate cùng firing. | [Grafana](screenshots/chaos-B-grafana.png) · [Hai alert](screenshots/prometheus-alert-firing.png) |
| C | Sau khi về baseline, đổi LLM_MODEL=mock-llm-large | 15:05:01 → 15:07:35, **154 s**, LLMCostBurnRateHigh | Cost burn rate 16.44 USD/giờ, p95 riêng LLM 495.9 ms. | [Grafana](screenshots/chaos-C-grafana.png) · [Alerts](screenshots/chaos-C-alerts.png) |
| D | Sau khi về baseline, pause một replica | 15:08:49 → 15:09:35, **46 s**, AgentInstanceDown | Instances up từ 2 xuống 1. Locust ghi 26 lỗi 504 cho /ask tại thời điểm quan sát. | [Grafana](screenshots/chaos-D-grafana.png) · [Alerts](screenshots/chaos-D-alerts.png) |
| E | Sau khi unpause, đổi AGENT_VERSION=v1 | Bắt đầu 15:10:17, quan sát đến 15:11:24. Ba rule agent-slo vẫn inactive. Cost alert còn firing từ trước E. | Hai replica v1, 17.66 req/s, 5xx 0.92%, p95 198.3 ms. Input 640.2 và output 349.4 tokens/s. | [Grafana](screenshots/chaos-E-grafana.png) · [Alerts](screenshots/chaos-E-alerts.png) |

A và B có điều kiện `for` lần lượt 1 và 2 phút. Thời gian đo còn gồm lúc thay container, cửa sổ PromQL, kỳ scrape/eval và độ trễ quan sát. Các tham số chaos truyền qua biến môi trường khi chạy Compose. Sau mỗi thay đổi độc lập, stack quay về giá trị baseline. Cửa sổ 5 phút của chi phí vẫn chứa dữ liệu từ model đắt sau khi cấu hình đã quay về mock-llm-small.

Trong D, Nginx log `[26/Nov/2026:08:08:59 +0000] "POST /ask HTTP/1.1" 504`. Nginx hết thời gian đọc upstream trong khi replica đang pause. Vì proxy tự tạo 504, agent không ghi HTTP status đó. Cùng thời điểm, panel error rate phía agent chỉ khoảng 0.39%.

Trong E, v1 bỏ retrieval. Với traffic gần bằng baseline, input từ 1286.5 xuống 640.2 tokens/s, output từ 683.8 xuống 349.4 tokens/s. Retrieval hit ratio còn hiển thị dữ liệu v2 trong cửa sổ 5 phút. Eval offline cho thấy 1/23 câu đạt ở v1 so với 21/23 ở baseline v2. Dùng eval định kỳ trên golden set và check regression trước merge để phát hiện giảm chất lượng này, vì latency và 5xx vẫn có thể đạt SLO.

### 4.3 · Jaeger và log

Ở đợt A, lấy trace dài nhất có thể đối chiếu log trong mẫu tìm kiếm theo service observable-agent. Jaeger hiển thị tiền tố ở tiêu đề. Nút Copy Trace ID cho kết quả đầy đủ khớp từng ký tự với trace_id trong dòng log.

- Trace chậm [d8f492c2c75cee5c4f5417fe7a91b16a](screenshots/jaeger-slow-trace.png) dài **1713.08 ms**. Span con chat mock-llm-small chiếm **1688.57 ms**, tức **98.57%**. Duration log gần tương ứng vì đo từ hàm mock. Span ID của log là ngữ cảnh đang hoạt động lúc ghi log, nên đối chiếu bằng trace_id.
- Trace lỗi [d54e36148ce48f8a71c55254c3bc5bae](screenshots/jaeger-error-trace.png) trả 503. Panel Details của span chat mock-llm-small hiển thị event exception do LLMError.

~~~json
{"ts": "2026-11-26T08:00:46.605887+00:00", "level": "INFO", "service": "observable-agent", "instance": "aff1f5739910", "event": "llm_call", "trace_id": "d8f492c2c75cee5c4f5417fe7a91b16a", "span_id": "d2321eb0afff7ed2", "request_id": "27080f569b64", "model": "mock-llm-small", "agent_version": "v2", "input_tokens": 83, "output_tokens": 44, "cost_usd": 3.9e-05, "llm_ms": 1689.2}
~~~

## 5. Benchmark scaling (production)

Locust headless 100 users, ramp 10 users/s, 2 phút mỗi lần. Dùng --no-deps để lệnh run giữ số replica đã chọn, chờ Prometheus thấy đủ target UP. Hàng Aggregated gộp cả /ask và /health.

| Instance | RPS | p50 (ms) | p95 (ms) | p99 (ms) | Failures / Requests |
|---:|---:|---:|---:|---:|---:|
| [1](benchmark-results/scale_1_stats.csv) | 65.47 | 190 | 520 | 1700 | 60 / 7767 (0.77%) |
| [3](benchmark-results/scale_3_stats.csv) | 66.02 | 190 | 260 | 1700 | 70 / 7846 (0.89%) |

Từ 1 lên 3 replica, p95 giảm 50%, RPS tăng khoảng 0.84%. p99 vẫn 1700 ms và app tạo lỗi 503 theo tỷ lệ mock. Truy vấn p95 LLM của panel tại lúc kết thúc từng lần đo lần lượt là 198.16 và 197.89 ms. Workload có thời gian nghỉ 0.5–2 giây giữa request và mỗi call LLM có delay mock riêng, nên thêm replica chủ yếu giảm chờ của request trong khoảng burst. Hai lần đo không đủ để quy toàn bộ khác biệt p95 cho riêng việc đổi số replica.

## 6. Kết luận

1. SLO có thể đạt ở 10 concurrent request và vỡ ở 50 dù RPS tăng. Đọc cả RPS lẫn percentile trước khi chọn mức tải.
2. Chỉ 3% slow request đã đẩy p99 từ 249.2 lên 1703.1 ms. Trace cho thấy span gọi mock LLM chiếm 98.57% thời gian của request chậm đã chọn.
3. Lượng token và tổng cost tăng khi dùng retrieval, nhưng chi phí trên mỗi câu đúng giảm từ 0.00040935 xuống 0.00003485 USD ở bản fixed.

Thêm counter và alert 5xx theo route ở lớp proxy. Nó đo phản hồi mà client thực sự nhận, gồm timeout 504 tạo tại Nginx khi agent chưa trả HTTP response.
