function b1 = LBa12(n,a1,b1,Or,bsr,T1,T22) %交配法之交換(選拆碳足跡)


RR=[];
c=[];
Bs=round(n*bsr); %Block-size
for i=1:n-Bs+1
    RR=a1(i:i+Bs-1); %第i個區間
%     SS=LBss1(Bs,GCT,Information,RR,L1,L2); %第i個區間適應值
%     SS =LBss1(T1,T22,RR);%%%
     SS =LBss3(RR,T1,T22);
    c=[c;RR SS i];
end

f=c(c(:,end-1)==min(c(:,end-1)),:); %找出適應值最小的區間
P=round(rand()*(size(f,1)-1)+1,0);
d=f(P,:);
b1(d(end):d(end)+Bs-1)=d(1:Bs); %把a1保留區間複製到b1相同位置

B1=[];
for i=d(end):d(end)+Bs-1 %找出區間外重複數值的位置
    B=find(b1==b1(i));
    if nnz(B)~=1
       B1=[B1 B(B~=i)];
    end
end
b1(B1)=[]; %移除區間外重複的數值
b1 = LBrr1(Or,n,b1);

for i=1:n
    d=[];
    e1=[];
    f=[];
    if isempty(find(b1==i))==1 %找出b缺少的數值
        for j=1:nnz(b1)+1 
            d=[b1(1:j-1) i b1(j:end)]; %將缺少的數值放入每個位置
            y = LBb2(d,n,Or); %判斷該位置是否可行
            if y==1
%                 SS = LBss1(n,GCT,Information,d,L1,L2); %計算適應值
%                  SS =LBss1(T1,T22,d);%%%
                  SS =LBss3(d,T1,T22);
                e1=[e1;d SS];
            end
        end
        f=e1(e1(:,end)==min(e1(:,end)),1:end-1); %選擇適應值最小
        P=round(rand()*(size(f,1)-1)+1,0);
        b1=f(P,:);
    end
end