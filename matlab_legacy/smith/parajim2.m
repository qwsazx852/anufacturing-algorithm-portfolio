function [a,b] = parajim2(x,y)
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
a=x(n)
b=y(n)