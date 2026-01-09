function [a,b] = LBb01(n,a,b,Or,mutation,T1,T22) %突變選拆(碳足跡計算部分)


c=[];
for i = 1:nnz(b)
    q=rand();
    if q<mutation
        P=round(rand()*(size(a,2)-size(a,2)/2)+size(a,2)/2,0);
        c=a(i,:);
        for i1=1:P
            p=round(rand()*(nnz(c)-1)+1,0);
            p1=c(p);
            c(p)=[];
            d=[];
            e1=[];
            f=[];
            
            aa1=find(Or(:,p1)==1)';
            aa2=find(Or(p1,:)==1);
            
            bb1=[];
            J1=0;
            while nnz(aa1)~=0 %找出最前面可放位置
                bb1=[bb1 find(c==(aa1(1)))];
                aa1(1)=[];
                J1=max(bb1);
            end
            
            bb2=[];
            J2=n;
            while nnz(aa2)~=0 %找出最後面可放位置
                bb2=[bb2 find(c==(aa2(1)))];
                aa2(1)=[];
                J2=min(bb2);
            end
            
            for j=J1+1:J2
                d=[c(1:j-1) p1 c(j:end)]; %將缺少的數值放入每個位置
%                      SS = LBss1(T1,T22,d);%%%
                     SS = LBss3(d,T1,T22);
                    e1=[e1;d SS];
            end
            f=e1(e1(:,end)==min(e1(:,end)),1:end-1); %選擇適應值最小
            P1=round(rand()*(size(f,1)-1)+1,0);
            c=f(P1,:);
        end
        a(i,:)=c;
%         b(i) = LBss1(T1,T22,a(i,:));%%%
         b(i)= LBss3(a(i,:),T1,T22);
    end
end