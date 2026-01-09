function initialize=antpart01(CAPITAL,F,Fmole)%初始費洛蒙
for i =1:CAPITAL
   for j =1:CAPITAL
   if i~=j
       F(i,j)= F(i,j)+Fmole ; 
   end
   end
end
initialize=F;