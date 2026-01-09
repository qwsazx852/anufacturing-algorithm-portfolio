a=[72,65,54,10,12];x=0;y=0;
for i=1:5
    if a(i)>=50
     x=x+1   
    elseif a(i)<=20 
     y=y+1
    end
end
c=10;d=10;
if x==3 && y==2
    d=0
    c=0
elseif x==3
    d=0
elseif x==2 
    c=0
end

