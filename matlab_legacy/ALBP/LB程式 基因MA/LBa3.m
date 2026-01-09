function [ee,bb] = LBa3(n,a,b,crossover,GCT,Information,chromosome,L1,L2,Or) %crossover MA交配法


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
        e=c(P1,:);
        [d,e] = LBa4(n,d,e,Or);
        SS = LBss1(n,GCT,Information,d,L1,L2);
%          SS = LBss1(GCT,Information,d)%%測試用
        a=[a;d];
        b=[b SS];
        SS = LBss1(n,GCT,Information,e,L1,L2);
%         SS = LBss1(GCT,Information,e)%%測試用
        a=[a;e];
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