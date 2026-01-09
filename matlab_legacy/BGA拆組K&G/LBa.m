function [ee,bb] = LBa(n,a,b,crossover,asb,asb2,chromosome); %crossover PPX選拆利潤


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
        O1=round(rand(1,n)+1,0);
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
        %
%         SS = LBss1(T1,T22,RR);
        SS = LBss4(asb,asb2,RR)
        a=[a;RR];
        b=[b SS];
        RR=[];
        for i=1:n
            if O1(i)==1
                RR(i)=d1(1);
            else
                RR(i)=e1(1);
            end
            d1(d1==RR(end))=[];
            e1(e1==RR(end))=[];
        end
        %
%          SS = LBss1(T1,T22,RR);
         SS = LBss4(asb,asb2,RR)
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