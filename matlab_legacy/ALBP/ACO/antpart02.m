function [step2,Onece2]=antpart02(CAPITAL,initialize,F1,a,b,destion)%狀態轉換(需要改公式)

for j =1:CAPITAL
    if j == 1
        cap1=1:CAPITAL;
        transform=randperm(CAPITAL,1)
        cap1(transform)=[]
        anttwo=[transform]
    else
         Tij=initialize(anttwo(j-1),cap1)
            dij=destion(anttwo(j-1),cap1)
            bigscore= ( Tij).^a.*(1./ dij).^b
        if rand()<F1%虛擬隨機比例規則
%             Tij=initialize(anttwo(j-1),cap1);
%             dij=destion(anttwo(j-1),cap1);
%             bigscore= ( Tij).^a.*(1./ dij).^b;
            delete=find(cap1==cap1(find(  bigscore==max(  bigscore),1)));
            anttwo=[ anttwo,cap1(delete)];
            cap1(delete)=[];
        else%隨機比例規則
            char= (bigscore);
%             for s =1:length(char)
%                 if char(s)==0
%                     char=char+Fmole.*0.01;%初始費洛蒙調整不為0後可省略
%                 end
%             end
%             mo=1./char
            mO=char./sum(char);
            ada=cumsum(mO);
            
            for m6 =1:length(char)
                if rand()<=ada(m6)
                    delete= find(char==char(m6),1);
                    break
                end
            end
            
            anttwo=[ anttwo,cap1(delete)];
            cap1(delete)=[];
        end
    end
end
step2=anttwo;
