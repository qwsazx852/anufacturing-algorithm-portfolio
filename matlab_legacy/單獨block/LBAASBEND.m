clc
clear
tic
%% 參數控制
chromosome = 20; %染色體數量 20
crossover = 0.7; %交配率  0.7
mutation = 0.9; %突變率   0.9
s =40; %迭代數
L1=0.6;
L2=0.4;
bsr = 0.6;
search=10;%鄰域搜尋代數
asb=[18];%選拆零件(利潤)
asb2=[1];%選拆零件(碳足跡)
%單一零件組拆裝成本


%% 釘書機
n = 18;  % 工作個數
order = [3 2;3 1;4 5;4 8;5 7;5 6;6 9;7 9;8 6;10 12;11 12;13 12;14 1;14 4;15 12;16 15;17 15;18 10;18 11;18 13];  %拆裝先後順序條件限制
order2=[1 3;1 14;2 3;4 14;5 4;6 5;6 8;7 5;8 4;9 6;9 7;10 18;11 18;12 10;12 11;12 13;12 15;13 18;15 16;15 17];%組裝先後順序條件限制
reuse=[2 5 9 7 13];% 重新使用
recycle=[3 4 6 8 10 11 12 14 16 17 18];%回收
T1=[3 1 2 3 4 3 3 3 3 3 1 1 1 2 4 2 2 3];%工具
T2=[2 -2 -2 2 -2 -1 1 2 1 -2 2 -2 -2 -2 -2 -2 -2 -3];%方向
%%  BOWMAN
% n = 8;  % 工作個數
% order = [1 2;2 3;2 4;3 5;3 6;4 6;5 7;6 8];  %先後順序條件限制
% Information = [11 17 9 5 8 12 10 3];  %各工作時間
% GCT = 20; %Given Cycle Time

%%
a=[];
a2=[];
b=[];
b2=[];
D=[];
x=[];
y=[];
Or = LBbn(order,n);
Or2= LBbn(order2,n);
T22= direction(T2,n);
for i1=1:s%% 原版
    i1
    for i=1:chromosome %隨機產生初始解
        RR = randperm(n);
        RR = LBrr1(Or,n,RR);
        RR2 = randperm(n);
        RR2 = LBrr1(Or2,n,RR2);
        SS =LBss1(T1,T22,RR);%選拆後零件成本
        SS2=LBss1(T1,T22,RR2);%組裝零件工具方向
        a=[a;RR];
        a2=[a2;RR2];
        b=[b SS];
        b2=[b2 SS2];
        
    end
    
    f=(1./b);
    cc=LBcc(f,chromosome); %輪盤法
    a=[a;a(cc,:)];
    a2=[a2;a2(cc,:)];
    b=[b b(cc)];
    b2=[b2 b2(cc)];
 %% 交配突變   
    [a,b] = LBa0(n,a,b,crossover,T1,T22,chromosome,Or,bsr); %交配(block)選拆後零件成本
    [a2,b2] = LBa0(n,a2,b2,crossover,T1,T22,chromosome,Or2,bsr); %交配2(block)組裝零件工具方向懲罰值
    [a,b] = LBb0(n,a,b,Or,T1,T22,mutation); %突變(block)拆
    [a2,b2] = LBb0(n,a2,b2,Or2,T1,T22,mutation); %突變2(block)組
%     c=[a,a2]%組拆順序
    B = LBss2(b,b2,chromosome);%利潤適應值    
    B2= LBss3(b,b2,chromosome);%耗能適應值
    B3=[]
    for p =1:chromosome
    B3=[B3,L1.* B(p)./ L2.*B2(p)];
    end
   A3=find(B3==max(B3));
   A1=find(B==max(B));
   A2=find(B2==max(B2));

    D = [D; LBSAVE(A3,B3,B,B2);LBSAVE(A1,B3,B,B2);LBSAVE(A2,B3,B,B2)];%每世代最佳適應值 
%     D2=

   
    
%     if i1 == 1
%         x=[x 0];%收斂圖參數(1)
%         y=[y f];%收斂圖參數(2)
%     else
%         if y(end) ~= f
%             x = [x i1];
%             y = [y y(end)];
%         end
%     end
%     y = [y f];
%     x = [x i1];
%     
end

f


% plot(x,y,'LineWidth',2)
% title('收斂圖')
% xlabel('代數')
% ylabel('適應值')

toc