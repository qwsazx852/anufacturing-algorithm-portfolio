clc;
clear;
% %% 四則運算
% a=1+6*5/4+7*(6-1)*(5^2)/(3*4)
% 
% 
% 
% %% P13 試題
% B=[ 1    2   3   4
%     5    6   7   8
%     9   10  11  12
%     13   14  15  16];
% %5的位置
% anser1_1=B(2)
% anser1_2=B(2,1)
% %取3;7;11;15(取第三列)
% anser2_1=B(:,3)
% anser2_2=B(3,:)
% 
% %% P14 試題
% 
% B=[ 1    2   3   4
%     5   12   7   6
%     9    6  11  12]
% 
% 
% [X Y]=size(B)
% max(B)
% min(B)
%  find(B==7)
%  find(B)
% % % length(B)
% % max(max(B))
% % min(min(B))
% % 
% % 
% % %% 作業一
% % 
% % A=[8  6  4  2
% %     1  3  5  7
% %     3  4  9  4];
% % 
% % B=[ 1    2   3   4
% %     5   12   7   6
% %     9    6  11  12];
% % 
% % % A_bigest=max(max(A))
% % % [X,Y]=find(A==A_bigest)
% % % Ans=[X,Y]
% % % B_bigest=max(max(B))
% % % [X,Y]=find(B==B_bigest)
% % % Ans=[X,Y]
% % 
% % % A(A>5)
% % % B(B>5)
% % E=[1 2 3 4 5;
% %     6 7 8 9 10]
% %    length(E)
% A = [ 3 5 1 7
%      6 2 2 5
%      
% 8 1 4 3 ] ;
% A_bigest=max(max(A))
% [X,Y]=find(A==A_bigest)
% [X,Y]
% A(A>5)
% vid=cell(1,40)
% a=size(vid{3},2)
% change_p=cell(1,40)
% 
% p_best=xid
% %     p_fitness_value=fitness_value;
% 
% 
% change_p{2}=[3,3]
%% 矩陣運算
% A = [1   ,  3   ,  5]
% A+5
% A-3
% A*2
% A/3
% A
% B = [2   ,  4   ,  6] 
% A+B
% A-B
% % A*B
% % A/B
% A.*B
% A./B



%% if示例(溫度)
% A=20
% output=[]
% if A<35
%     output=["溫度過低"]
% elseif A>36.5&&A<38
%     output=["溫度正常"]
% else
%     output=["溫度過高"]
% end
%% for示例
save=[]%為儲存亂數之空矩陣
for i =1:10 %進行10次
    r=rand %rand指令為0~1間之亂數
    save=[save;r]%每跑完一次就儲存一次r
end
%% for練習
% prompt="請輸入數字"
% x = input(prompt)
% add=0
% for i =1:length(x)
%     add=add+x(i)
% end
% add


 %% 試題
% A=34
% B=20
% if A>60&&B>60%如果A>60
%     C=2
% elseif 40<A&&A<60||40<B&&B<60%如果A和B其中有一介於40~60之間
%     C=1%C=1
% else%非以上兩種狀況
%     C=0%C=0
% end
% C

%% 作業二
% A=90
% if A >40
%     A=A+5
%     if A>60
%         A=A+10
%         if A>80
%             A=A-30
%         end
%     end
% end
% A





%% word例題一(迴圈寫法)
% prompt="請輸入數字或矩陣"
% A = input(prompt)
% A=[3,12,5,4,1,21,15]
% c_add=0
% for i =1:length(A)
%    if A(i)<=5
%        c=1
%    else
%        c=2
%    end
%       c_add=c_add+c   
% end
%% 7/20練
% c=[70 65 54 20 30]
% % c=[50 70 20 40 45]
% % c=[72 65 54 10 12]
%  Dsave=0
%  Csave=0
%  for i =1:length(c)
%      if c(i)>50
%          Dsave=Dsave+1
%          if Dsave>=3
%              D=0
%          end
%      elseif c(i)<20
%          Csave=Csave+1
%          if Csave>=2
%              C=0
%          end
%      end
%  end    
%%  7/20
% C=0
% B = [ 62 , 85 , 72 , 42 , 75 , 94 , 42 ]
% for i =1:length(B)-1
%     if B(i)>B(i+1)
%         C=C+1
%     elseif B(i)<B(i+1)
%         C=C-1
%     end
% end
% C
%% 7/20 (2)
C=0
B = [ 62 , 85 , 72 , 42 , 75 , 94 , 42 ]
for i =1:length(B)-1
    for j =i+1:length(B)
        if B(i)>B(j)
            C=C+(j-i)
        elseif B(i)<B(j)
            C=C-(j-i)
        end
    end
end
    
%% while
a=0
while a<10%重複運算至a>=10
    a=a+2
end
a
%% 0727(1)
% c=[-8 -15 6 -4 7 -6 -9]   
% add=0
% for i =1:length(c)
%   while c(i)<=0
%    c(i)=c(i)+2   
%       add=add+1
%   end
% end
%% 0727(2)
c=randperm(2) 
for j =1:2
    for i =1:length(c)
        if c(i)>7
            c(i)=0
        else
%           break%跳出i回到j
%            return%跳出i不回到j
           continue%跳到下一runi
        end
    end
end
%% 0727(3)
save=[]
a=1:100
for i =1:100
    i
    if mod(i,6)==0%6的倍數
        save=[save,i] 
         continue
    elseif mod(i,2)~=0&&mod(i,3)~=0%非2、3的倍數
         save=[save,i]
    end
   
end
a(unique(save))=[]
%%
% a=[]
% for i =200:300
%    if mod(i,12)==0&&mod(i,18)==0 
%     a=[a,i]
%    end
% end
% a

%% 0727(4)
% c=876215;
% add=0
% for i =1:6
%     add=add+mod(c,10)
%     c=(c-mod(c,10))/10       
% end
% add
% %% 0727(質數)
% a=[]
% for i =1:100
%     u=0
%     for j =1:i
%         if mod(i,j)==0
%             u=u+1
%             if u>2
%              break
%             end
%         end
%     end
%     if u<=2
%         a=[a,i]
%     end 
% end
% a
% %%  大到小
% A=[7,6,3,8,4,5,3,7]
% B=[]
% while ~isempty(A)
% B=[B,max(A)]
% A(find(A==max(A),1))=[]
% end