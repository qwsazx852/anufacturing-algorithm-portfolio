function [aa,bb,cc]=fitness(fxm_ans,T1,T22,PP) ;%(n,CT,minisec,fxm_ans,L1,L2,PP)
aa=[];
bb=[];
cc=[]; 
reference_point=[350,0.001];%r參考點釘書機:150，印表機1800
for i=1:PP %隨機產生初始解  
    R=[];
    a = fitness1(fxm_ans{i},T1,T22);%%以利潤中止點決定適應值
    b = fitness2(fxm_ans{i},T1,T22);%%以碳足跡中止點決定適應值
   
   R1=[sqrt((reference_point(1)-a(1))^2+(reference_point(2)-a(2))^2)];
   R2=[sqrt((reference_point(1)-b(1))^2+(reference_point(2)-b(2))^2)];
    R=[R,R1,R2];
    if R1<=R2
         bb=[bb a(1)];
         cc=[cc a(2)];
    else
         bb=[bb b(1)];
         cc=[cc b(2)];
    end


    aa=[aa min(R)];
  
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