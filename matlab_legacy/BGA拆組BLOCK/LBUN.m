function [f1,f2] = LBUN(a,b) %凌越解分級
aa=[];
bb=[];
c=[];
b2=[];

for c1= 1:length(a)
    addd=0;
    cp1=b(c1,:);
    if c1==1
        cp2=2:length(a);
    elseif c1==length(a)
        cp2=1:length(a)-1;
    else
        cp2=[1:(c1-1),(c1+1):length(a)];
    end

    for c2= 1:length(cp2)
        if cp1(1)>b(cp2(c2),1)&&cp1(2)<b(cp2(c2),2);
            addd=addd+1;
        end
         
    end
    aa=[aa;addd]; 
end

% for c= 1:length(a)
%  aa=[aa;length(find(b(c,1)>b(:,1)))];
%  bb=[bb;length(find(b(c,2)<b(:,2)))];
% end
% aa=aa+bb
% aaa=aa
% aa=aa+bb
aaa=aa;
        










%% 等級區分  
%等級一
level1=[];
level1=[level1;find(aa==max(aa))];
de=find(aaa==max(aaa));
aaa(de)=1;
%等級二
level2=[];
level2=[level2;find(aaa==max(aaa))];
de=find(aaa==max(aaa));
aaa(de)=1;
%等級三
level3=[];
level3=[level3;find(aaa>1)];
%% 擁擠距離計算

add=1
for run1=1:3
    score=[];
    if run1==1
        level=level1;
    elseif run1==2
        level=level2;
        add=add+2;
    else
        level=level3;
        add=add+2;
    end
    for run=1:length(level)
        ans=b(level(run),:);
        score=[score;ans];
         c=[c;a(level(run),:)];
    end
    for run=1:length(level)
        b2=[b2;(max(score(:,1))-b(level(run,1)))+b(level(run,1),2)-(min(score(:,2)))+add];
    end
end
f=find(b2==min(b2),1);
f1=a(f,:);
f2=b(level1(f),:);



%% 剩a和適應值計算以及輪盤
