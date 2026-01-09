function [a,b] = LBb4(n,a,b,Or,GCT,Information,mutation,L1,L2) %mutation 隨機取一段顛倒


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
        bl1=min(p,p1);
        bl2=max(p,p1);
        bl3=fliplr(c(bl1:bl2));
        c(bl1:bl2)=bl3;
        y = LBb2(c,n,Or);
        if y==2
            c = LBrr1(Or,n,c);
        end
        a(i,:)=c;
        b(i) = LBss1(n,GCT,Information,a(i,:),L1,L2);
%         b(i) = LBss1(GCT,Information,a(i,:));%%測試用
    end
end