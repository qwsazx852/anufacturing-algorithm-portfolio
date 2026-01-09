function a=fitness(n,CT,minisec,fxm_ans,L1,L2,PP) ;%(fxm_ans,minisec,CT,PP)
a=[];
for i=1:PP %隨機產生初始解  
    SS = LBss1(i,CT,minisec,fxm_ans,L1,L2); 
    a=[a SS];
end


% a=[];
%     for j=1:length(fxm_ans)
%         
%         all=0;
%         factory=1;
%         Y1=fxm_ans{1,j};
%         for ja =1:length(Y1)
%        
%          all=minisec(Y1(ja))+all;
%          if all>CT
%              all=minisec(Y1(ja));
%              factory= factory+1;
%          end
%         end
% 
%        a=[a,factory];%論盤適應值    
%     end
%    