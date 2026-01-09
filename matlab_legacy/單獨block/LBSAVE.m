function SS = LBSAVE(A3,ONE,TWO,THREE); %計算適應值(拆裝工具和方向性)

SS=[];
for i = 1:length(A3)
   SS=[SS;ONE(A3(i)),TWO(A3(i)),THREE(A3(i))] ;
end