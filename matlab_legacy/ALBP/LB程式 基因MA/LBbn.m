function Or = LBbn(order,n)

CA=cell(n,1);
bn=[];
for i=1:n
%     i
    if sum(order(:,1)==i) ~= 0
        ww=[order(order(:,1)==i,2)' 10000];
        xx=[order(order(:,1)==i,2)' order(order(:,1)==ww(1),2)'];
        while sum(ww) ~= 10000
            ww=[ww(1:end-1) order(order(:,1)==ww(1),2)' ww(end)];
            ww(1)=[];
            ww=unique(ww);
            xx=[xx order(order(:,1)==ww(1),2)'];
            xx=unique(xx);
        end
        bn(i)=nnz(xx);
        CA{i,1}=xx;
    else
        bn(i)= 0;
    end
end

Or=zeros(n);
for i=1:n
    for j=1:nnz(CA{i})
        Or(i,CA{i}(j))=1;
    end
end