function [step301,step302, initialize]=antpart03(CAPITAL,step2,HOTF,destion,antdestion,antskechle,F)%局部更新
 destionA=0;
for k = 1:CAPITAL-1
%     
%     if k==CAPITAL
%        break
%     else
        destionA= destionA+destion(step2(k),step2(k+1));
        F(step2(k),step2(k+1))=(1-HOTF).*F(step2(k),step2(k+1))+HOTF.*(1./step2(end));%局部更新公式
%     end
end
%  destionA= destionA+step2(1)
antdestion=[antdestion; destionA];
step301=antdestion;
antskechle=[antskechle; step2];
step302=antskechle;
initialize=F;
end
