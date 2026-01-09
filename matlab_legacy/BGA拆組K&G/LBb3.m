function [a,b] = LBb3(n,a,b,Or,T1,T22,mutation) %mutation 隨機兩點交換突變法


c=[];
for i = 1:nnz(b)
    q=rand();
    if q<mutation
        c=a(i,:);
        p=round(rand()*(n-1)+1,0);
        p1=round(rand()*(n-1)+1,0);
        while p==p1
            p1=round(rand()*(n-1)+1,0);
        end
        d=c(p);
        c(p)=c(p1);
        c(p1)=d;
        y = LBb2(c,n,Or);
        if y==2
            c = LBrr1(Or,n,c);
        end
        a(i,:)=c;
        SS = LBss1(T1,T22, a(i,:));
    end
end