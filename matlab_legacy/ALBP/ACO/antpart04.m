function [best1,F]=antpart04(CAPITAL,F,HOTF,antscore,antPP)%全域更新
best1=find(antscore==(min(antscore)),1);
best= antPP(best1,:);
for m =1:CAPITAL-1
        F( best(m), best(m+1))=(1-HOTF).* F( best(m), best(m+1))+ F( best(m), best(m+1));  
end
% best1=find(antscore==(min(antscore)),1);
% step4=best1;
end
