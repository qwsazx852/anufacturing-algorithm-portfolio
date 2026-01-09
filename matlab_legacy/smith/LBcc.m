function cc = LBcc(f,chromosome) %輪盤法


cc=[];
f = f/sum(f); %機率權重
for i=1:chromosome
    P = rand();
    d = 1;
    c = f(1);
    while c < P
        d = d+1;
        c = c+f(d);
    end
    cc = [cc d];
end