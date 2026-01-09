function y = LBb2(RR,n,Or) %判斷是否符合優先順序(y=1符合，y=2不符合)


for i=1:nnz(RR)
    for j=i+1:nnz(RR)
        if Or(RR(j),RR(i))==1
            y=2;
            return
        end
    end
end
y=1;