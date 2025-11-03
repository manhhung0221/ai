Tốt lắm 💪 — đây là **bản hướng dẫn chi tiết Tuần 1** để bạn nắm nền tảng “agent” đúng chuẩn kỹ thuật chứ không chỉ thuộc lòng định nghĩa.

---

## 🗓 Tuần 1 – **Hiểu bản chất của Agent trong AI**

### 🎯 Mục tiêu

* Biết chính xác “agent” là gì, tại sao nó là đơn vị trung tâm của AI.
* Phân biệt được các loại agent: Reflex – Model-based – Goal-based – Utility-based.
* Hiểu vòng lặp **Perceive → Decide → Act → Learn** – nền tảng của mọi AI agent.
* Viết được 1 “reflex agent” nhỏ trong Python.

---

### 💡 1. Kiến thức lý thuyết trọng tâm

1. **Định nghĩa:**
   Agent là một thực thể **quan sát môi trường**, **ra quyết định (hành động)** và **học từ phản hồi** để tối đa mục tiêu.
   Môi trường → Cảm biến (percept) → Bộ não (agent function) → Bộ chấp hành (actuator).

2. **Loại agent (theo AIMA – Russell & Norvig):**

   | Loại          | Đặc điểm                         | Ví dụ                                           |
   | ------------- | -------------------------------- | ----------------------------------------------- |
   | Reflex        | Hành động theo luật if–else      | Robot hút bụi: nếu “dirty” → “Hút”              |
   | Model-based   | Có bộ nhớ về trạng thái hiện tại | Xe tự lái biết vị trí mình ở ngã tư             |
   | Goal-based    | Tối ưu đường đến mục tiêu        | Google Maps chọn đường ngắn nhất                |
   | Utility-based | Tối đa mức độ hài lòng           | Trading bot chọn lệnh tối đa lợi nhuận / rủi ro |

3. **Khái niệm PEAS:**

   * **Performance measure** (chỉ số đánh giá)
   * **Environment**
   * **Actuators**
   * **Sensors**

4. **Vòng lặp cốt lõi:**

   ```
   while True:
       percept = sense(environment)
       action = decide(percept, memory)
       environment = act(action)
       learn(percept, reward)
   ```

---

### 🧠 2. Thực hành: Reflex Agent đầu tiên

**Bài toán:** robot hút bụi trên lưới 2D – nếu vị trí bẩn → hút, nếu sạch → di chuyển ngẫu nhiên.

```python
import random, time

class Environment:
    def __init__(self, n=3):
        self.grid = [[random.choice(['clean', 'dirty']) for _ in range(n)] for _ in range(n)]
        self.n = n
    def is_dirty(self, x, y): return self.grid[x][y] == 'dirty'
    def clean(self, x, y): self.grid[x][y] = 'clean'

class ReflexVacuumAgent:
    def __init__(self): self.score = 0
    def perceive_and_act(self, env, x, y):
        if env.is_dirty(x, y):
            env.clean(x, y)
            action = 'CLEAN'
            self.score += 10
        else:
            action = 'MOVE'
            x, y = random.randrange(env.n), random.randrange(env.n)
            self.score -= 1
        return x, y, action

env = Environment()
agent = ReflexVacuumAgent()
x, y = 1, 1

for step in range(10):
    x, y, action = agent.perceive_and_act(env, x, y)
    print(f"Step {step}: {action} at ({x},{y}) | Score={agent.score}")
    time.sleep(0.3)
```

🔍 Quan sát: Agent chỉ phản xạ tức thời, không học.
👉 Ở tuần 2 ta sẽ cho agent “nhớ” và “ra quyết định” bằng LLM.

---

### 📘 3. Tài nguyên đọc thêm

* *Artificial Intelligence: A Modern Approach* – Chương 1–2.
* MIT 6.034 Lecture 1: Introduction to AI (YouTube).
* Blog: “Understanding Intelligent Agents” – Medium / towardsdatascience.

---

### 🧩 4. Bài tập tuần 1

1. Mô tả PEAS cho 3 hệ thống: Trading Bot, Chatbot hỗ trợ khách hàng, Drone giao hàng.
2. Mở rộng Reflex Agent:

   * Thêm bộ nhớ (xem lần nào đã đi qua).
   * Thêm thưởng/phạt khi lặp lại ô đã sạch.
3. Viết một đoạn ngắn (200 từ) so sánh: Reflex vs Goal-based agent.

---

### 📈 5. Kết quả cuối tuần

✅ Hiểu vòng đời agent.
✅ Phân loại được các kiểu agent.
✅ Code được agent đơn giản.
✅ Biết “LLM agent” chính là bản mở rộng của các khái niệm này.

---

Nếu bạn muốn, mình sẽ viết luôn **Week 2 Guide** — “Làm chủ LLM và Prompt Engineering” với ví dụ thật (ChatGPT API + function calling → agent phân tích CSV). Bạn có muốn chuyển sang tuần 2 luôn không?
