function RR = LBjudgment(n,order,Information,PP,AF,BT,q0,GCT,bn)  %螞蟻路徑


RR = [];
while nnz(RR) < n
    OP = LBlookfor(order,RR,n);
    P = round(rand()*(nnz(OP)-1)+1,0);
    if isempty(RR) == 1
        RR = OP(P);
    else
        if nnz(OP) > 1
            q = rand();
            a = [];
            bb = bn(OP(:));
            for i = 1:nnz(OP)
                if sum(bb)~=0
                    a(i) = PP(RR(end),OP(i))^AF*(Information(OP(i))/GCT+bn(OP(i))/max(bb))^BT;
                else
                    a(i) = PP(RR(end),OP(i))^AF*(Information(OP(i))/GCT)^BT;
                end
            end
            if q <= q0
                a1 = find(a == min(a));
                P1 = round(rand()*(nnz(a1)-1)+1,0);
                RR = [RR OP(a1(P1))];
            else
                a = a/sum(a);  %機率權重
                P2 = rand();
                b = 1;
                c = a(1);
                while c < P2
                    b = b+1;
                    c = c+a(b);
                end
                RR = [RR OP(b)];
            end
        else
            RR = [RR OP];
        end
    end
    order(order(:,1) == RR(end),:) = [];
end