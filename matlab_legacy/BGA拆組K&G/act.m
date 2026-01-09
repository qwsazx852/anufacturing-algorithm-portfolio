function [ans,ans2] = act(SS0,SS1);


r=[0.5,0.5]; %決策偏好

x=SS0(:,1)
y=SS0(:,2)
% z=SS0(:,3);
plot(x,y,'.','MarkerSize',20)
xlabel('f1','FontName','Times New Roman')
ylabel('f2','FontName','Times New Roman')
zlabel('f3','FontName','Times New Roman')
grid on

f=[];
for i=1:2
    if i==1
        f(i)=max(SS0(:,i))+((1-r(i))*(max(SS0(:,i))-min(SS0(:,i))))

    else
        f(i)=min(SS0(:,i))+((1-r(i))*(max(SS0(:,i))-min(SS0(:,i))))
    end
end
f;
f1=repmat(f,size(SS0,1),1)
r1=repmat(r,size(SS0,1),1)
d=r1.*((f1-SS0).^2)
d1=[]
for i1=1:size(SS0,1)
    d1=[d1;i1 sum(d(i1,:))^(1/2)]
end

a=d1(d1(:,2)==min(d1(:,2)),:)
ans=SS0(a(1),:)
ans2=SS1(a(1),:)