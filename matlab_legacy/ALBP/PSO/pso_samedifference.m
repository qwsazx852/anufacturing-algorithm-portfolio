function fxm_ans2=pso_samedifference(fxm_ans,fym_ans,fzm_ans,n,Or,c1,c2);%w
% n=75
% w=0.8
fxm_ans2=cell(1,length(fxm_ans));
for j=1:length(fxm_ans)    
    change=[fxm_ans{j}];
    SSV1=zeros(1,n);
    for i =1:n
        if rand<c1
            if fxm_ans{j}(i)==fym_ans(i)
                SSV1(i)=fym_ans(i);
                
            end
        end
        if rand<c2
            if fxm_ans{j}(i)==fzm_ans(i)
                SSV1(i)=fzm_ans(i);
            end
        end
    end
    if length(find(SSV1~=0))>0
        a=find(SSV1>=1);
        for run1=1:length(a)
            if length(a)==1
                ch=change(a(run1)+1:end);
                ch=ch(randperm(length(ch)));
                change(a(run1)+1:end)=LBrr1(Or,n,ch);
%                  ANS2= [ ANS2, a(run1),LBrr1(Or,n,ch)]
                break
            end
           
            if run1==1
                if a(run1)==1
                 ch=change(a(run1)+1:a(run1+1)-1); 
                 ch=ch(randperm(length(ch)));
                 change(a(run1)+1:a(run1+1)-1)=LBrr1(Or,n,ch);
%                 ANS2= [ ANS2, a(run1),LBrr1(Or,n,ch)]
                
                else
                ch=change(1:a(run1)-1);
                ch=ch(randperm(length(ch)));
                change(1:a(run1)-1)=LBrr1(Or,n,ch);
%                   ANS2= [ ANS2,LBrr1(Or,n,ch),a(run1)]
                end
            elseif run1==length(a)
              ch=change(a(run1)+1:end);
              ch=ch(randperm(length(ch)));
              change(a(run1)+1:end)=LBrr1(Or,n,ch);
%                 ANS2= [ ANS2,a(run1),LBrr1(Or,n,ch)]
            else
             ch=change(a(run1)+1:a(run1+1)-1);%開始可能有值，結束可能還有值
             ch=ch(randperm(length(ch)));
             change(a(run1)+1:a(run1+1)-1)=LBrr1(Or,n,ch);
%              ANS2= [ ANS2,a(run1),LBrr1(Or,n,ch),a(run1+1)]
            end
           
        end
        
        
    end
    fxm_ans2{j}= change;
end

% end