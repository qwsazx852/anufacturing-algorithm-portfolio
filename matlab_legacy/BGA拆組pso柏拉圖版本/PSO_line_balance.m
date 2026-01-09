tic
clc;
clear;
%% 參數設置

PP=100;%初始族群數
ger=1000;%迭代數
w=0.8;%慣性權重
L1=0.6;
L2=0.4;
c1=0.5;%自我學習因子
c2=0.5;%群體學習因子
mutation=0.8
%% hv參數設置
U = [1200,0.001];%每次需修改釘書機[350,0.001]，印表機[1800，0.001]
AU = [0,100];
% 設置樣本數量
N = 1000;
% function hv = hypervolume(F, AU, U, N)
% 雙目標hypervolume計算函數
% F: 待測的Pareto前緣，是一個n_sol x 2的矩陣，第一列表示利潤，第二列表示碳足跡
% AU: antiutopia點，是一個1 x 2的行向量，表示最不理想的利潤和碳足跡
% U: utopia點，是一個1 x 2的行向量，表示最理想的利潤和碳足跡
% N: 抽樣數量，用於近似計算hypervolume值
[n_sol, dim] = size(U);
samples = bsxfun(@plus, AU, bsxfun(@times, (U - AU), rand(N, dim)));
%% 釘書機
% n = 18;  % 工作個數
% order = [3 2;3 1;4 5;4 8;5 7;5 6;6 9;7 9;8 6;10 12;11 12;13 12;14 1;14 4;15 12;16 15;17 15;18 10;18 11;18 13];  %拆裝先後順序條件限制
% order2=[1 3;1 14;2 3;4 14;5 4;6 5;6 8;7 5;8 4;9 6;9 7;10 18;11 18;12 10;12 11;12 13;12 15;13 18;15 16;15 17];%組裝先後順序條件限制
% reuse=[2 5 9 7 13];% 重新使用
% recycle=[3 4 6 8 10 11 12 14 16 17 18];%回收
% T1=[3 1 2 3 4 3 3 3 3 3 1 1 1 2 4 2 2 3];%工具
% T2=[2 -2 -2 2 -2 -1 1 2 1 -2 2 -2 -2 -2 -2 -2 -2 -3];%方向
%% 吊扇
n=26;
order = [5 1; 5 2;5 3;5 4;6 4;11 7;11 18;12 7;12 18;15 7;15 18;16 7;16 18;19 22;19 23;19 24;20 22;20 23;20 24;21 22;21 23;21 24;26 25;4 7;25 17;7 8;7 9;18 17;8 10;8 14;9 10;9 14;17 14;10 13;14 13];%限制排序
T1=[2 2 2 1 1 1 1 1 1 3 1 1 3 3 1 1 1 1 1 1 1 1 1 1 4 2];%工具
T2=[2 3 -3 3 2 2 3 3 3 3 3 3 -3 -3 -3 -3 -3 -3 -3 -3 -3 -3 -3 -3 -3 -3 ];%方向

%% 印表機
% n=52;
% order = [16 50;13 20;13 19;27 42;1 46;8 9;5 6;45 50;36 52;1 45;27 28;13 25;33 41;13 24;13 21;13 22;1 2;2 5;4 18;5 27;2 27;27 38;27 31;1 3;12 13;27 40;27 41;27 43;27 37;31 36;1 47;26 27;5 18;1 51;10 11;5 8;5 10;13 14;28 44;13 23;28 29;27 39;49 50;3 17;48 51;19 24;20 25;3 4;28 30;32 40;34 42;35 43;21 24;14 23;2 4;26 37;29 30;5 7;27 36;3 15;3 12;22 25]%限制排序
% T1=[1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 1 2 2 2 2 1 1 2 1 1 2 2 1 2 2 1 2 2 2 2 2 2 1 2 2 2 2 2 2 1 2 2 2 2 1 2 2];%工具
% T2=[ 2 2 2 -2 1 1 -1 2 1 1 1 -1 2 2 1 -2 -2 -2 -2 2 2 2 2 2 2 -2 2 2 -2 2 -2 1 1 1 1 1 -2 -2 1 2 2 2 2 -2 2 3 -3 3 2 2 -3 2];%方向


%% 程式start
T22= direction(T2,n);
fsave=[];
% for tast =1:10%重複測試
    tic
 Or = LBbn(order,n);

 %% 初始族群

 fxm_ans=PSO_ALBP01(PP,n,Or);

%% 適應值計算
[fxm,a,b]=fitness(fxm_ans,T1,T22,PP);%各別碳足跡與利潤之R-metric，fxm_ans=1x100cell，length=零件數
%每個個體之歷史最佳適應值
%% NPSO
D=[];
x=[];
y=[];
D2=[];
%% 拆
fym=min(fxm);%p-best
fzm=fym;%gbest適應值
fym_ans= fxm_ans{(find(fxm==min(fxm),1))};%p-best解排序
fzm_ans= fym_ans;%gbest解排序
for i1 = 1:ger
   i1 
%% 拆裝
    fxm_ans2=pso_samedifference(fxm_ans,fym_ans,fzm_ans,n,Or,c1,c2);%同中求異
     [score2,a,b]=fitness (fxm_ans2,T1,T22,PP);%適應值         
    [fxm,fym, fzm,fxm_ans, fym_ans,fzm_ans]=pso_anser (fym_ans,fxm_ans, fzm_ans,fxm,fym,fzm,fxm_ans2,score2,w);
%     if i1>=2
%         for ii=1:length(A(:,1))
%             fxm_ans{PP+ii}=a1(ii,:);
%         end
%         [score2,a,b]=fitness (fxm_ans,T1,T22,PP+length(A(:,1)));%適應值
%     end
    
   %% hypervolume
HV=[];
[A,P2] = p(a',b');
for i =1:length(A(:,1))
    hv = hypervolumetwo(A(i,:),samples); 
    HV=[HV;hv];
end
x2=A(:,1);
y2=A(:,2);
a1=[];
b1=[];
for j =1:length(P2)
 a1=[a1;fxm_ans{P2(j)} ];
 b1=[x2,y2];
end
%% 保留柏拉圖解並產生新初始族群

% fxm_ans=PSO_ALBP01(PP,n,Or);
% 
% for ii=1:length(A(:,1))
%     fxm_ans{(PP+ii)}=a1(ii,:);
%     fxm=[fxm,b1(ii)]
% end
% PP=PP+length(A(:,1))
%% 絕對距離判斷代數中止
[R] = Rmetric(A)
%% hv收斂圖
B =max(HV)

D = [D B(1)];
f1=max(D);

if i1 == 1
    x=[x 0];
    y=[y f1];
else
    if y(end) ~= f1
        x = [x i1];
        y = [y y(end)];
    end
end
y = [y f1];
x = [x i1];
%% R收斂圖
% B =min(R)
%% 需留著
if i1==1
    qq=find(R==min(R),1)
    best={cell2mat(fxm_ans(qq)),[a(qq),b(qq)],min(R)}
else
    qq=find(R==min(R),1);
    B(1)
    min(D)
    if B(1)> max(D)
        best={cell2mat(fxm_ans(qq)),[a(qq),b(qq)],min(R)}
    end
end
 %% 鄰域搜尋  
%  if i1>500
%      if B<=max(D)
%          B2=0;
%          add=0;
%          while  B2<=max(D)
%              HV=[]
%              a= LBb222(n,fxm_ans,a,b,Or,T1,T22,PP,mutation); %突變TAX
%              [fxm,a,b]=fitness(a,T1,T22,PP);
%              for i =1:length(a)
%                  hv = hypervolumetwo([a(i),b(i)],samples);
%                  HV=[HV;hv];
%              end
%              B2=max(HV)
%              max(D)
%              add=add+1
% 
%              if add==100
%                  D = [D B2];%每世代最佳適應值
%                  f = max(D)
%                  beststop=LBssR(fzm_ans,T1,T22,samples)
%                  return
%              end
% 
%          end
% %          B=B2;
%      end
%  end
%% 
% D = [D B(1)];
% f1=min(D);
% 
% if i1 == 1
%     x=[x 0];
%     y=[y f1];
% else
%     if y(end) ~= f1
%         x = [x i1];
%         y = [y y(end)];
%     end
% end
% y = [y f1];
% x = [x i1];
%% 利潤收斂圖
% B =max(x2);
% D = [D B(1)];
% f1=max(D);
% if i1 == 1
%     x=[x 0];
%     y=[y f1];
% else
%     if y(end) ~= f1
%         x = [x i1];
%         y = [y y(end)];
%     end
% end
% y = [y f1];
% x = [x i1];
%% 碳足跡收斂圖
% B1=min(y2);
% D2= [D2 B1(1)];
% 
% f2=min(D2);
% if i1 == 1
%     x=[x 0];
%     y=[y f2];
% else
%     if y(end) ~= f2
%         x = [x i1];
%         y = [y y(end)];
%     end
% end
% y = [y f2];
% x = [x i1];
    
%     D = [D B];%每世代最佳適應值
%     f = min(D);
end

 ans = parajim(x2,y2);
% f
plot(x,y,'LineWidth',2)
title('收斂圖')
xlabel('代數')
ylabel('適應值')
beststop=LBssR(fzm_ans,T1,T22,samples)
% end

% p_best=min(score)
% find(score==min(score),1)
% before_fxm=cell(1,ger)
% before_fxm{1}=[before_fxm{1},score]
 toc    
    
    
    
    
    
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
     



