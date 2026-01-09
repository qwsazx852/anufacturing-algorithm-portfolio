function [a,b] = LBb(n,a,b,Or,T1,T22,mutation) %mutation 隨機兩點交換突變法
bb=cell(100,2);

c=[];
for i = 1:length(a)
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
%        b(i,:) = LBss2(a(i,:),T1,T22);
%        b(i,2) = LBss3(a(i,:),T1,T22);%
       bb{i,1}= LBss2(a(i,:),T1,T22);bb{i,2}=LBss3(a(i,:),T1,T22);
    end
end