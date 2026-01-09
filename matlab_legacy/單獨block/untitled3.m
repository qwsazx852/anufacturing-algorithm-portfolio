b=[62,85,72,42,75,94,42];c=0
for i=1:6
    for z=i+1:7
   if b(i)<b(z)
       c=c-(z-i)
   elseif b(i)>b(z)
       c=c+(z-i)
   end
    end
end
