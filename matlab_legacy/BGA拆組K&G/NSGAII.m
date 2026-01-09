clc
clear
tic
%% 參數控制
chromosome = 100; %染色體數量
crossover = 0.8; %交配率
mutation = 0.2; %突變率
s =1000; %迭代數
asb=[18];%選拆零件(利潤)
asb2=[1];%選拆零件(碳足跡)
%% hv參數設置
U = [1800,0.001];%每次需修改釘書機[350,0.001]，印表機[1800，0.001]
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
% n=26;
% order = [5 1; 5 2;5 3;5 4;6 4;11 7;11 18;12 7;12 18;15 7;15 18;16 7;16 18;19 22;19 23;19 24;20 22;20 23;20 24;21 22;21 23;21 24;26 25;4 7;25 17;7 8;7 9;18 17;8 10;8 14;9 10;9 14;17 14;10 13;14 13];%限制排序
% T1=[2 2 2 1 1 1 1 1 1 3 1 1 3 3 1 1 1 1 1 1 1 1 1 1 4 2];%工具
% T2=[2 3 -3 3 2 2 3 3 3 3 3 3 -3 -3 -3 -3 -3 -3 -3 -3 -3 -3 -3 -3 -3 -3 ];%方向
%% 印表機
n=52;
order = [16 50;13 20;13 19;27 42;1 46;8 9;5 6;45 50;36 52;1 45;27 28;13 25;33 41;13 24;13 21;13 22;1 2;2 5;4 18;5 27;2 27;27 38;27 31;1 3;12 13;27 40;27 41;27 43;27 37;31 36;1 47;26 27;5 18;1 51;10 11;5 8;5 10;13 14;28 44;13 23;28 29;27 39;49 50;3 17;48 51;19 24;20 25;3 4;28 30;32 40;34 42;35 43;21 24;14 23;2 4;26 37;29 30;5 7;27 36;3 15;3 12;22 25]%限制排序
T1=[1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 1 2 2 2 2 1 1 2 1 1 2 2 1 2 2 1 2 2 2 2 2 2 1 2 2 2 2 2 2 1 2 2 2 2 1 2 2];%工具
T2=[ 2 2 2 -2 1 1 -1 2 1 1 1 -1 2 2 1 -2 -2 -2 -2 2 2 2 2 2 2 -2 2 2 -2 2 -2 1 1 1 1 1 -2 -2 1 2 2 2 2 -2 2 3 -3 3 2 2 -3 2];%方向

%% 程式撰寫處
a=[];
a2=[];
b=cell(100,2);
b2=[];
D=[];
D2=[];
x=[];
y=[];
f1=[];
f2=[];
Or = LBbn(order,n);
% Or2= LBbn(order2,n);
T22= direction(T2,n);
for i=1:chromosome %隨機產生初始解

    RR = randperm(n);
    RR = LBrr1(Or,n,RR);
    SS1 = LBss2(RR,T1,T22);
    SS2 = LBss3(RR,T1,T22)%選拆
    a=[a;RR];
    b{i,1}=SS1;b{i,2}=SS2;
end
for i1=1:s
    i1
    if i1 >=2
        for i=1:length(A(:,1)) %隨機產生初始解
             SS1 = LBss2(RR,T1,T22);
            SS2 = LBss3(RR,T1,T22);%選拆
             b{i,1}=SS1;b{i,2}=SS2;
        end

        for i=1:chromosome-length(A(:,1)) %隨機產生初始解
            RR = randperm(n);
            RR = LBrr1(Or,n,RR);
            SS1 = LBss2(RR,T1,T22);
            SS2 = LBss3(RR,T1,T22);%選拆
            a=[a;RR];
            b{i,1}=SS1;b{i,2}=SS2;
        end
    end
    %% 擁擠距離
    for i=1:chromosome
        SS1 = LBss2(a(i,:),T1,T22);
        SS2 = LBss3(a(i,:),T1,T22);%選拆
        b{i,1}=SS1;b{i,2}=SS2;
    end
    bb=[];
   for j =1:length(a)
      bb=[bb;b{j,2}];
   end
    
    a=cown(a,bb);
    %% 交配突變
    [a,b] = ppx(n,a,crossover,T1,T22);%交配選拆後    
    [a,b] = LBb(n,a,b,Or,T1,T22,mutation);%突變選拆後
   
    %% 擁擠距離
% % %         a=[a;a2]
% % %         b=[[b',c'];[b2',c2']]
%         [f1,f2] = LBUN(b(:,1),b(:,2))
%         D1=[D1;f1]
%         D=[D;f2]
   
%% hypervolume
% %%hv參數設置
% U = [350,0.001];
% AU = [0,1];
% % 設置樣本數量
% N = 1000;
% % function hv = hypervolume(F, AU, U, N)
% % 雙目標hypervolume計算函數
% % F: 待測的Pareto前緣，是一個n_sol x 2的矩陣，第一列表示利潤，第二列表示碳足跡
% % AU: antiutopia點，是一個1 x 2的行向量，表示最不理想的利潤和碳足跡
% % U: utopia點，是一個1 x 2的行向量，表示最理想的利潤和碳足跡
% % N: 抽樣數量，用於近似計算hypervolume值
% [n_sol, dim] = size(U);
% samples = bsxfun(@plus, AU, bsxfun(@times, (U - AU), rand(N, dim)));
%% STAR
HV=[];
aaa=[];
bbb=[];
for t=1:100
aaa=[aaa;b{t,1}(1,1);b{t,2}(1,1)];
bbb=[bbb;b{t,1}(1,2);b{t,2}(1,2)];
end
aaa;
bbb;
[A,P2] = p(aaa,bbb);
for i =1:length(A(:,1))
    hv = hypervolume(A(i,:),samples);
    HV=[HV;hv];
end
x2=A(:,1);
y2=A(:,2);
a1=[];
b1=[];
% b1=cell(100,2);
for j =1:length(P2)
 a1=[a1;a(P2(j),:) ];
end
for j =1:length(P2)
 b1=[b1;b(P2(j),:) ];
end
a=a1;
b=b1;
%% 絕對距離判斷代數中止
[R] = Rmetric(A);
%% hv收斂圖
B =max(HV);

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
% B =min(R);
%% save
if i1==1
    qq=find(R==min(R),1);
    best={a(qq,:),b(qq,:),min(R)};
else
    qq=find(R==min(R),1);
    B(1);
    min(D);
    if B(1)< min(D)
        best={a(qq,:),b(qq,:),min(R)};
    end
end
 %% 鄰域搜尋  
%  if i1>100
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
% 
%                  beststop=LBssR(s,T1,T22,inputp,samples)
%                  return
%              end
% 
%          end
% %          B=B2;
%      end
%  end
%% R
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
end
% stop=cell(100,2)
% for ii =1:length(a(:,1))
% [SS,SSs] = LBssR(a(ii,:),T1,T22)
% stop{ii,1}=SS;stop{ii,2}=SSs
% end
%% 看本次最佳柏拉圖解中止點
% s=best{1}(1,:)
% inputp=cell2mat(best{2}(1))
% 
% beststop=LBssR(s,T1,T22,inputp,samples)
% SS= taxlbss(s,samples,T1,T22)
% psoans=[]
% for iii =1:length(A)
% beststop=LBssR(a1(iii,:),T1,T22,A(iii,:),samples)
% psoans=[psoans;beststop]
% end
%  ans =parajim(x2,y2);
% 
% % f
% 
plot(x,y,'LineWidth',2)
title('收斂圖')
xlabel('代數')
ylabel('HV')
% best
% toc
% beststop
[ans,ans2]=act(A,a1);
beststop=LBssR(ans2,T1,T22,samples)
ans
ans=["NSGA-II"]