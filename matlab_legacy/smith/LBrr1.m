function RR = LBrr1(Or,n,RR) %產生可行解


for i=1:nnz(RR)
    for j=i+1:nnz(RR)
        if Or(RR(j),RR(i))==1
            b=RR(j);
            RR(j)=RR(i);
            RR(i)=b;
        end
    end
end