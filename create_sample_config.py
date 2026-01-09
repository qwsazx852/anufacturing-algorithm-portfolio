import pandas as pd
import numpy as np

def create_sample_excel():
    """
    建立一個範例的 'config.xlsx' 檔案，包含兩個工作表：
    1. Parameters: 存儲全域變數 (族群大小、交配率等)
    2. Constraints: 存儲優先順序限制 (Job A 必須在 Job B 之前)
    """
    
    # 1. 建立 Parameters 工作表
    params_data = {
        "Name": ["NUM_JOBS", "POPULATION_SIZE", "MAX_GENERATIONS", "CROSSOVER_RATE", "CYCLE_TIME"],
        "Value": [18, 100, 100, 0.8, 20],
        "Description": ["零件數 (Jobs)", "族群大小 (Population)", "迭代數 (Generations)", "交配率 (0.0-1.0)", "週期時間 (GCT)"]
    }
    df_params = pd.DataFrame(params_data)
    
    # 2. 建立 JobTimes 工作表
    # 定義 18 個作業的時間 (範例數據)
    times_data = {
        "JobId": list(range(1, 19)),
        "Time": [11, 17, 9, 5, 8, 12, 10, 3, 15, 7, 6, 14, 18, 4, 9, 11, 13, 8]
    }
    df_times = pd.DataFrame(times_data)

    # 3. 建立 Constraints 工作表 (模擬原本的 precedence_constraints)
    constraints_data = {
        "Predecessor": [3, 3, 4, 4, 5, 5, 6, 7, 8, 10, 11, 13, 14, 14, 15, 16, 17, 18, 18, 18],
        "Successor":   [2, 1, 5, 8, 7, 6, 9, 9, 6, 12, 12, 12, 1, 4, 12, 15, 15, 10, 11, 13]
    }
    df_constraints = pd.DataFrame(constraints_data)
    
    # 寫入 Excel 檔案
    output_file = "config.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_params.to_excel(writer, sheet_name="Parameters", index=False)
        df_times.to_excel(writer, sheet_name="JobTimes", index=False)
        df_constraints.to_excel(writer, sheet_name="Constraints", index=False)
        
    print(f"成功建立範例設定檔: {output_file}")
    print("您可以打開此檔案修改參數，無須更動 Python 程式碼。")

if __name__ == "__main__":
    create_sample_excel()
