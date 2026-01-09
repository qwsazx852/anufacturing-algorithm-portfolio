function OP = LBlookfor(order,RR,n)  %尋找下一可行節點


OP = 1:n;
for i = 1:nnz(RR)
    OP(OP==RR(i))=[];
end
for i = 1:nnz(order(:,1))
    OP(OP == order(i,2)) = [];
end