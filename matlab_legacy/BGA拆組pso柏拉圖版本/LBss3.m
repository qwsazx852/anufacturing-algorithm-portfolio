function SS = LBss3(b,b2); %計算適應值(拆裝工具和方向性)
Cs=0.0001413889;%% 拆裝時間乘碳係數
%% 拆裝時間
SS1=min(b);
LC=60;
LC=LC+SS1;
%% 組裝時間
SS2=min(b2);
DC=48;
DC=DC+SS2;
%% 碳足跡
SS=(LC+DC).*Cs;