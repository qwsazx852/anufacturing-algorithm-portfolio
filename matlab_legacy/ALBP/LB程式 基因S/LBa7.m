function [d,e] = LBa7(n,d,e) %SA(2000)交配法之交換


P=[];
P(1) = round(rand()*(n-1-1)+1,0);
P(2) = round(rand()*(n-1-1)+1,0);
while P(2)==P(1)
    P(1) = round(rand()*(n-1-1)+1,0);
end

rd1=d(1:min(P));
rd2=d;
rd3=d(max(P)+1:n);
rd4=[rd1 rd3];
re1=e(1:min(P));
re2=e;
re3=e(max(P)+1:n);
re4=[re1 re3];

for i=1:nnz(rd4)
    rd2(rd2==re4(i))=[];
    re2(re2==rd4(i))=[];
end

d=[rd1 re2 rd3];
e=[re1 rd2 re3];