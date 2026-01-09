function [fxm,fym, fzm,fxm_ans, fym_ans,fzm_ans]=pso_anser (fym_ans,fxm_ans, fzm_ans,fxm,fym,fzm,fxm_ans2,score2,w);
for i =1:length(fxm_ans)
    if rand<w
        if fxm(i)> score2(i)
            fxm(i)=score2(i);
            fxm_ans{i}=fxm_ans2{i};
        end
        if min(score2)<fym
            fym=min(score2);
            fym_ans=fxm_ans2{find(score2==min(score2),1)};
        end
        if fym<fzm
            fzm=fym;
            fzm_ans=fym_ans;
        end
    end
end
% if min(score2)<fym
%     fym=min(score2);
%     fym_ans=fxm_ans2{find(score2==min(score2),1)};
% end
% if fym<fzm
%     fzm=fym
%     fzm_ans=fym_ans
% end



