function ans=fitness(fxm_ans,T1,T22,PP) ;%(n,CT,minisec,fxm_ans,L1,L2,PP)
aa=[];
ans=[]; 
R=[];
% reference_point=[1200,0.001];%r參考點釘書機:150，印表機1800
for i=1:2:PP.*2 %隨機產生初始解  
  
    a = fitness1(fxm_ans{i},T1,T22);%%以利潤中止點決定適應值
    b = fitness2(fxm_ans{i},T1,T22);%%以碳足跡中止點決定適應值  
    ans=[ans;a;b];
    
  
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