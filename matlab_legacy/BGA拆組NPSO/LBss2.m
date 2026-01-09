function SS = LBss1(n,GCT,Information,RR,L1,L2) %計算適應值


CT = 0;
OR = [];
tn = 0; %最小工作站數
Ti = []; %各工作站工作時間
for i = 1:nnz(RR)
    if CT+Information(RR(i)) <= GCT
        CT = CT+Information(RR(i));
    else
        tn=tn+1;
        Ti(tn) = CT;
        CT = Information(RR(i));
    end
end
tn=tn+1;
Ti(tn) = CT;

SS = (((sum((GCT-Ti).^2))/tn)^(1/2))*L1-(sum(Ti)/(tn*GCT))*L2;