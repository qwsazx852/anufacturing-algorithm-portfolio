% 假設我們有一個解集X，其中有5個解，每個解有3個目標值
X = [1 2 3; 4 5 6; 7 8 9; 10 11 12; 13 14 15];

% 假設我們希望計算的參考點為(16, 17, 18)
ref = [16 17 18];

% 使用MATLAB中的hv()函數計算HV
hv_value = hypervolume(X, ref);

% 將計算結果顯示出來
disp(['HV value: ' num2str(hv_value)]);