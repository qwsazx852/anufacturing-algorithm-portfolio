function [ee,bb] = LBa5(n,a,b,crossover,GCT,Information,chromosome,L1,L2) %crossover MA基本交配法


c=a;
for j=1:size(a,1)/2
    q=rand();
    P = round(rand()*(size(c,1)-1)+1,0);
    P1 = round(rand()*(size(c,1)-1)+1,0);
    while P1==P
        P1 = round(rand()*(size(c,1)-1)+1,0);
    end
    if q<crossover
        d=c(P,:);
        d1=c(P,:);
        e=c(P1,:);
        e1=c(P1,:);
        O=round(rand(1,n)+1,0);
        RR=[];
        for i=1:n
            if O(i)==1
                RR(i)=d(1);
            else
                RR(i)=e(1);
            end
            d(d==RR(end))=[];
            e(e==RR(end))=[];
        end
        SS = LBss1(n,GCT,Information,RR,L1,L2);
%         SS = LBss1(GCT,Information,RR)%%測試用
        a=[a;RR];
        b=[b SS];
        RR=[];
        for i=1:n
            if O(i)==1
                RR(i)=e1(1);
            else
                RR(i)=d1(1);
            end
            d1(d1==RR(end))=[];
            e1(e1==RR(end))=[];
        end
        SS = LBss1(n,GCT,Information,RR,L1,L2);
%         SS = LBss1(GCT,Information,RR)%%測試用
        a=[a;RR];
        b=[b SS];
    end
    if P<P1
        c(P,:)=[];
        c(P1-1,:)=[];
    else
        c(P1,:)=[];
        c(P-1,:)=[];
    end
end

ee=[];
bb=[];
for i= 1:chromosome
    dd=find(b==min(b));
    f=dd(unidrnd(nnz(dd)));
    ee=[ee;a(f,:)];
    bb=[bb b(f)];
    a(f,:)=[];
    b(f)=[];
end