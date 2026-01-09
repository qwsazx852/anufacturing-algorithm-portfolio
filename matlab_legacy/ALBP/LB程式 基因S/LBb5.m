function [a,b] = LBb5(n,a,b,Or,GCT,Information,mutation,L1,L2) %SA(2000)¬ðÅÜªk


c=[];
for i=1:nnz(b)
    q=rand();
    if q<mutation
        c=a(i,:);
        P=round(rand()*(n-1-1)+1,0);
        c1=c(1:P);
        c2=c(P+1:end);
        Or1=Or;
        for i1=1:nnz(c1)
            Or1(c1(i1),:)=0;
        end
        while nnz(c1)~=n
            c4=[];
            c21=nnz(c2);
            for j=1:c21
                if sum(Or1(:,c2(j)))==0
                    c4=[c4 c2(j)];
                    c2(j)=0;
                end
            end
            c2(c2==0)=[];
            for i1=1:nnz(c4)
                Or1(c4(i1),:)=0;
            end
            bb=randperm(nnz(c4));
            c4=c4(bb);
            c1=[c1 c4];
        end
        SSc1 = LBss1(n,GCT,Information,c1,L1,L2);
        if SSc1<b(i)
            a(i,:)=c1;
            b(i) = LBss1(n,GCT,Information,a(i,:),L1,L2);
        end
    end
end