function [ans,ans2] =cown(axx,b)

c=1:length(b);
c=c';
bb=[];
for i= 1:length(b)
    bb=[bb;b(i,:),c(i)];
end
b=bb;
b1=[];
x=b(:,1);
y=b(:,2);
z=b(:,3);
delete=[];
save1=[];
save1anser=[];
save2=[];
save2anser=[];
save3=[];
save3anser=[];
x1=x;
y1=y;
z1=z;
long=length(b);
for ii =1:2
    x=x1;
    y=y1;
    z=z1;
    delete=[];
    for i =1:length(x1)

        for j =1:length(x1)
            
            if x1(i)<x1(j)&&y1(i)>y1(j)
                delete=[delete,i];
                break
            end
        end
    end
  
    x1=x1(delete);
    y1=y1(delete);
    z1=z1(delete);
    x(delete)=[];
    y(delete)=[];%2905.47606666667  0.00648975051000000
    z(delete)=[];
    if ii==1
        save1=[save1;x,y];%% 等級一
        save1anser=[ save1anser;z];
    elseif ii==2
        save2=[save2;x,y];%% 等級二
        save2anser=[ save2anser;z];
     save3=[save3;x1,y1]; %% 等級三
     save3anser=[ save3anser;z1];
    end
end
[a,b,c]=Dsave(save3(:,1),save3(:,2),save3anser);%% 等級三計算擁擠距離

save3b= calculateCrowdingDistance(length(save3), [a,b]);
 %%目前做到計算完等級三擁擠距離，只差輪盤法跟補上每一條的母體順序
    cc=LBcc(save3b,length(save3));
anser=c(cc);
theanser=[];
ans2=[];
for s=1:length(save1anser)
    theanser=[theanser;axx(save1anser(s),:)];
end
 ans2=[ ans2;save1];
for s=1:length(save2anser)
    theanser=[theanser;axx(save2anser(s),:)];
end
 ans2=[ ans2;save2];
for s=1:length(anser)
theanser=[theanser;axx(anser(s),:)];
ans2=[ans2; save3(cc(s),:)];
end
ans=theanser;
ans3=cell(1,length(ans));
for run =1;length(ans);
    ans3{run}=ans(run);
end
ans=ans3;
