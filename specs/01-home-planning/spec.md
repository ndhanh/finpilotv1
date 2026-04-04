# Feature: Home Planning (Mua Nhà)

## 1. Purpose

Giúp người dùng trả lời câu hỏi:

> “Tôi có thể mua nhà khi nào?”

Feature này tập trung vào:

- tạo “wow moment” nhanh (<60s)
- chuyển đổi user sang trả tiền

---

## 2. Success Metrics

- Conversion rate (free → paid): ≥ 3%
- Completion rate (input → result): ≥ 70%
- Time to first result: < 60 seconds

---

## 3. Scope

### Included (MVP)

- Input tài chính cơ bản
- Tính toán timeline mua nhà
- Hiển thị kết quả nhanh (summary)
- Paywall cho kế hoạch chi tiết

### Excluded (Future)

- Monte Carlo simulation
- Banking integration
- Multi-user (couple planning)

---

## 4. User Flow

### Step 1 — Input

User nhập thông tin cơ bản

### Step 2 — Instant Result

Hiển thị:

- năm có thể mua nhà
- timeline đơn giản

### Step 3 — Comparison

Hiển thị:

- nếu không plan → trễ X năm

### Step 4 — Paywall

User phải trả tiền để:

- xem chi tiết
- xem kế hoạch tối ưu

---

## 5. User Inputs

### Required

| Field           | Type   | Example     |
| --------------- | ------ | ----------- |
| age             | number | 28          |
| monthly_income  | number | 20,000,000  |
| current_savings | number | 200,000,000 |
| monthly_saving  | number | 5,000,000   |

---

### Optional (default)

| Field             | Default       |
| ----------------- | ------------- |
| house_price       | 3,000,000,000 |
| down_payment_rate | 20%           |

---

## 6. Business Logic

### 6.1 Down Payment
