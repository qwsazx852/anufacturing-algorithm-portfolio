# 📄 Resume Integration Guide: Algorithm Engineer Portfolio

為了讓您的履歷在投遞「演算法工程師」或「AI 工程師」職缺時脫穎而出，請參考以下的撰寫策略。重點在於**強調核心邏輯的研發能力**，並將 Web 部分作為「具有落地能力的加分項」。

---

## 🇹🇼 104 人力銀行特別攻略 (104 Specific Strategy)

在 104 上，您有三個關鍵位置可以「置入」這個作品集：

### 1. 作品集/連結欄位 (Portfolio Link) - **最重要**
*   在 104 履歷編輯畫面的 **「附件/作品集」** 或 **「個人網站」** 欄位。
*   **標題**：`GitHub: Manufacturing Optimizer (Python)`
*   **網址**：`https://github.com/qwsazx852/anufacturing-algorithm-portfolio` (記得確認網址正確)
*   *這是人資 (HR) 第一眼會點擊的地方。*

### 2. 專案成就 (Project Achievements)
*   104 有專門的 **「工作經歷」** -> **「專案成就」** 區塊。
*   請在這裡新增一個專案：
    *   **專案名稱**：Python 智慧製造排程演算系統 (Smart Manufacturing Scheduler)
    *   **職務類別**：演算法工程師
    *   **專案描述**：
        > 針對 NP-Hard 產線平衡問題，開發 GA/PSO/ACO/SA 四種啟發式演算法。
        > 1. **核心演算法 (FROM SCRATCH)**：不依賴套件，純手刻演算法邏輯，設計 Transitive Closure 矩陣解決複雜的工序相依性限制。
        > 2. **效能優化 (PERFORMANCE)**：設計 SPV 編碼規則將連續型 PSO 應用於離散排程，並導入 Vibe Coding 工作流加速全端開發。
        > 3. **完整程式碼 (CODE)**：`https://github.com/qwsazx852/anufacturing-algorithm-portfolio`

### 3. 自傳 (Autobiography)
*   在自傳的**第一段或最後一段**，一定要放連結。因為很多傳統主管習慣只看自傳。
*   **範例寫法**：
    > ...為了深入研究啟發式演算法在實際工業問題的應用，我近期獨立開發了一套「智慧製造排程系統」，實作了基因演算法與蟻群演算法。完整的程式碼架構與演算法邏輯，歡迎參考我的 GitHub 作品集：`github.com/qwsazx852/...`

---

## 📝 英文/通用履歷 (General Resume / PDF)

### 🔗 Header / Contact Info
*   **GitHub**: 建議放可點擊的連結。
*   如果這是您唯一的或最核心的作品，可以在聯絡資訊旁直接加上：`Portfolio: Manufacturing-Optimization-Solver`

### 📂 Projects Section (專案經歷)
這區塊最重要。請直接複製或微調以下內容：

**Project Title: Smart Manufacturing Schedule Optimizer** (Python, Meta-Heuristics)
*   **Developed and benchmarked 4 meta-heuristic algorithms (GA, PSO, ACO, SA) from scratch** to solve the NP-Hard "Assembly Line Balancing Problem" (ALBP).
*   **Engineered a custom topological repair mechanism**, ensuring 100% validity of generated schedules under strict precedence constraints (DAG).
*   **Designed hybrid encoding strategies**, including SPV (Smallest Position Value) rule to adapt continuous PSO particle vectors to discrete job sequences.
*   **Deployed as a Microservice**: Productized the research engine into a REST API using FastAPI. Leveraged AI-assisted workflows to rapidly prototype a React-based visualization dashboard for real-time convergence monitoring.

---

## 💡 面試自我介紹策略 (The Pitch)

當面試官問到這個專案時，您的敘述邏輯應該是：

1.  **"I identified a problem..."** (製造業排程很難，是 NP-Hard 問題...)
2.  **"Research to Production..."** (我最初用 MATLAB 驗證了演算法的數學正確性，確認可行後，再將其移植 (Porting) 到 Python 進行產品化開發。這顯示我有紮實的研究基礎，也有落地的工程能力。)
3.  **"I built the core engine..."** (我手寫了 GA/PSO 等演算法，處理了最難的 Constraints 矩陣...)
4.  **"I delivered a product..."** (為了展示效果，我用 AI 輔助快速搭建了 Web 介面。這顯示我不只懂演算法，也有軟體工程思維。)

---
*Created by Antigravity for Jun - 2026*
