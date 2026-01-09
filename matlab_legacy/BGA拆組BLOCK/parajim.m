function ans = parajim(x,y)
delete=[];
for i =1:length(x)
   
    for j =1:length(x)
        j
        if x(i)<x(j)&&y(i)>y(j)
            delete=[delete,i]
            break
        end
    end
end
x(delete)=[]
y(delete)=[]%2905.47606666667  0.00648975051000000
dsave=[]
for i =1:length(x)
    
d=sqrt((x(i))^2+(y(i))^2)
dsave=[dsave,d]
   
end

b1=sort(dsave)
n=[]
for i=1:length(dsave)
find(dsave==b1(i))
n=[n,find(dsave==b1(i))]
end
x=x(n)
y=y(n)



% 繪製所有解的散點圖
scatter(x, y);

% 使用plot()函數繪製曲線
hold on;
plot(x, y, 'b--');
hold off;
% % 繪製Pareto前沿上的解
% hold on;
% scatter(pareto_front(:,1), pareto_front(:,2), 'filled', 'r');
% hold off;

% 添加圖例和標籤
legend( 'Pareto front');%'All solutions',
xlabel('Objective 1');
ylabel('Objective 2');