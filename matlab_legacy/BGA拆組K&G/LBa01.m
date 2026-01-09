function [ee,bb] = LBa01(n,a,b,crossover,T1,T22,chromosome,Or,bsr) %crossover工具方向變換


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
        RR = LBa1(n,d,e,T1,T22,Or,bsr);%%%
%         SS =LBss4(asb,asb2,RR)
        SS =LBss1(T1,T22,RR);
        a=[a;RR];
        b=[b SS];
        RR=[];
        RR = LBa1(n,e,d,T1,T22,Or,bsr);%%%
%        SS =LBss4(asb,asb2,RR)
        SS =LBss1(T1,T22,RR);
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