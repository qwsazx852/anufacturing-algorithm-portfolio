function T22= direction(T2,n) %方向懲罰值
% n=18;
% T2=[2	-2	-2	2	-2	-1	1	2	1	-2	2	-2	-2	-2	-2	-2	-2	-3];
% T22=zeros(n);
for i =1:n
    for j =1:n
        if -T2(i)==T2(j)
            T22(i,j)=2 ;         
        elseif T2(i)~=T2(j)
            T22(i,j)=1 ; 
        else
            T22(i,j)=0 ;
        end
    end
end