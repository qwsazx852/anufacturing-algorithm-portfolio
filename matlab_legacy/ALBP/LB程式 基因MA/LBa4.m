function [d,e] = LBa4(n,d,e,Or) %MA交配法之交換


rd1=d(1:fix(n/3));
rd2=d(fix(n/3)+1:n-fix(n/3)-1);
rd3=d(n-fix(n/3):n);
d=[rd3 rd1 rd2];

re1=e(1:fix(n/3));
re2=e(fix(n/3)+1:n-fix(n/3)-1);
re3=e(n-fix(n/3):n);
e=[re3 re1 re2];

for i=1:nnz(rd2)
    d(d==re2(i))=[];
    e(e==rd2(i))=[];
end

rd4=d(end-nnz(rd1)+1:end);
rd5=d(1:end-nnz(rd1));

re4=e(end-nnz(rd1)+1:end);
re5=e(1:end-nnz(rd1));

d=[re4 rd2 re5];
e=[rd4 re2 rd5];

d = LBrr1(Or,n,d);
e = LBrr1(Or,n,e);