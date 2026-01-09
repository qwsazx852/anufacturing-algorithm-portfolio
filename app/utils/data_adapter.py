import pandas as pd
import os
from typing import Dict, List, Tuple, Any

class ConfigLoader:
    """
    負責從外部來源 (Excel, DB) 讀取設定檔的適配器 (Adapter)。
    目前實作：Excel 讀取功能。
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def load_config(self) -> Dict[str, Any]:
        """
        讀取 Excel 設定檔，回傳包含參數與限制的字典。
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"找不到設定檔: {self.file_path}，請先執行 create_sample_config.py 建立它。")
            
        print(f"正在讀取設定檔: {self.file_path} ...")
        
        # 讀取 Parameters 工作表
        df_params = pd.read_excel(self.file_path, sheet_name="Parameters")
        
        # 將參數轉換為字典，例如: {'NUM_JOBS': 18, 'POPULATION_SIZE': 100}
        config = {}
        for _, row in df_params.iterrows():
            name = row['Name']
            value = row['Value']
            config[name] = value
            
        # 讀取 Constraints 工作表
        df_constraints = pd.read_excel(self.file_path, sheet_name="Constraints")
        
        # 將限制轉換為 list of tuples: [(3, 2), (3, 1), ...]
        constraints_list = []
        for _, row in df_constraints.iterrows():
            pre = int(row['Predecessor'])
            suc = int(row['Successor'])
            constraints_list.append((pre, suc))
            
        config['CONSTRAINTS'] = constraints_list
        
        # 讀取 JobTimes 工作表 (若存在)
        try:
            df_times = pd.read_excel(self.file_path, sheet_name="JobTimes")
            # 確保按照 JobId 排序，這樣索引 0 對應 Job 1
            df_times = df_times.sort_values(by="JobId")
            config['TIME_INFO'] = df_times['Time'].tolist()
        except ValueError:
            print("警告: 找不到 'JobTimes' 工作表，TIME_INFO 將為空。")
            config['TIME_INFO'] = []
        
        return config

    # 未來可以擴充：
    # def load_from_mysql(self, connection_string):
    #     ...
