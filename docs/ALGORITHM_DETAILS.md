# 智慧製造排程與拆解優化系統 (Intelligent Manufacturing Scheduling & Disassembly Optimization System)
> **基於元啟發式演算法的自動化排程與拆解平衡系統**

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Service-green?style=flat&logo=fastapi)
![Algorithm](https://img.shields.io/badge/Algorithm-Meta--Heuristics-orange?style=flat)

## 📖 專案概述 (Project Overview)
本專案旨在解決製造業中經典的 **NP-Hard** 優化問題：**裝配線平衡問題 (Assembly Line Balancing, ALBP)** 以及 **選擇性拆解規劃 (Selective Disassembly Planning)**。

給定一系列具有特定 `處理時間 (process_times)` 和嚴格 `優先順序限制 (precedence_constraints)`（例如：工序 A 必須在工序 B 之前完成）的工單，目標是在滿足 `週期時間 (Cycle Time)` 的限制下，將工序分配到 **最少的工作站 (Workstations)**，或是在拆解過程中最大化回收利潤並最小化碳排放。

本系統從零實作 (From Scratch) 並比較了七種先進的元啟發式演算法：

1.  **遺傳演算法 (GA)**：演化搜尋，結合客製化的雙點交配 (Two-Point Crossover) 與修復邏輯。
2.  **粒子群優化 (PSO)**：群體智慧，使用 **SPV (Smallest Position Value)** 規則將連續空間映射至離散工序。
3.  **蟻群優化 (ACO)**：基於費洛蒙的建設性啟發式演算法，模擬工序路徑選擇。
4.  **模擬退火 (SA)**：物理激發的機率搜尋，作為單一解軌跡搜尋的基準。
5.  **多目標 PSO (NPSO)**：針對 **選擇性拆解規劃** 的進階求解器，使用 Hypervolume 指標同時優化 **利潤** 與 **碳足跡**。
6.  **區塊式 GA (Block-Based GA)**：使用保留邏輯結構的區塊交配與貪婪突變，進行高精度的局部序列挖掘。
7.  **Kang & Genetic Algorithm (K&G)**：實作優先權保留交配 (PPX)，針對拆解序列提供極佳的收斂速度與限制條件處理能力。

核心引擎封裝於 **FastAPI 微服務** 中，提供可即時呼叫的 RESTful API 介面。

---

## 🏗️ 系統架構 (System Architecture)

### 1. 核心求解器 (The Core Solvers - Python)
-   **模組化設計**: 所有演算法皆繼承自統一介面，確保擴充性。
-   **強健的限制處理**: 內建客製化的 `Transitive Closure (傳遞閉包)` 矩陣建構器，確保所有生成的排程（染色體/粒子）皆為合法的拓樸排序 (Topological Sort)。
-   **高效能運算**: 在 PSO 速度更新等向量運算中大量使用 `NumPy`。

### 2. 微服務層 (The Microservice - FastAPI)
-   提供 API 端點 (如 `/optimize/ga`, `/optimize/pso`) 供遠端調用。
-   回傳標準 JSON 格式的排程結果，包含 `min_stations` (最小工作站數) 與最佳 `sequence` (工序排列)。
-   包含 Swagger UI 供互動測試。

---

## 📊 效能基準測試 (Performance Benchmark)

| 演算法 | 平均執行時間 | 特色 | 適用場景 |
| :--- | :--- | :--- | :--- |
| **Simulated Annealing (SA)** | ~0.05s | 快速，單解邏輯 | 即時且簡單的重排程任務 |
| **Genetic Algorithm (GA)** | ~0.30s | 強健的群體搜尋 | 複雜限制、大規模問題 |
| **PSO** | ~1.00s | 連續空間搜尋 | 適合可有效映射 SPV 編碼的問題 |
| **ACO** | ~3.00s | 建構式啟發法 | 路徑依賴性極強的圖論問題 |
| **NPSO (Multi-Obj)** | ~1.50s | Pareto 優化 (利潤 vs 碳排) | 逆向物流、綠色選擇性拆解 |
| **Block-Based GA** | ~6.00s | 區塊交配 + 貪婪突變 | 高精度的局部搜尋 |
| **K&G (PPX)** | ~0.50s | 優先權保留交配 (PPX) | **最佳效能：** 在 Stapler 案例中取得最高 HV 值 |

---

## 🛠️ 技術棧 (Technology Stack)
-   **語言**: Python 3.x
-   **核心庫**: NumPy (數學運算), Matplotlib (視覺化), Pandas (數據處理)
-   **Web 框架**: FastAPI, Pydantic (資料驗證)
-   **演算法實作**: 純手寫實作 (Custom Implementation)，未使用任何黑箱優化庫。

---

## 📬 聯絡資訊 (Contact)
**演算法工程師**: Jun
**專注領域**: 智慧製造 AI、作業研究 (OR)、智慧決策系統。
