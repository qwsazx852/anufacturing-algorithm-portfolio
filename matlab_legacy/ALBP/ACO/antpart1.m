%% 初始族群
clc;
clear;


% destion=[0,4,6,3;2,0,6,9;1,9,0,6;5,6,7,0];
destion=[0,153,510,706,966,581,455,70,160,372,157,567,342,398;
        153,0,422,664,997,598,507,197,311,479,310,581,417,376;
        510,422,0,289,744,390,437,491,645,880,618,374,455,211;
        706,664,289,0,491,265,410,664,804,1070,768,259,499,310;
        966,997,744,491,0,400,514,902,990,1261,947,418,635,636;
        581,598,390,265,400,0,168,522,634,910,593,19,284,239;
        455,507,437,410,514,168,0,389,482,757,439,163,124,232;
        70,197,491,664,902,522,389,0,154,406,133,508,273,355;
        160,311,645,804,990,634,482,154,0,276,43,623,358,498;
        372,479,880,1070,1261,910,757,406,276,0,318,898,633,761;
        157,310,618,768,947,593,439,133,43,318,0,582,315,464;
        567,581,374,259,418,19,163,508,623,898,582,0,275,221;
        342,417,455,499,635,284,124,273,358,633,315,275,0,247;
        398,376,211,310,636,239,232,355,498,761,464,221,247,0];%距離矩陣
antp=100;%螞蟻數量
CAPITAL=14;%城市數量
F=zeros(CAPITAL,CAPITAL)%費洛蒙矩陣
PP=100;%世代數0
F1=0.8;%狀態轉換機率
HOTF=0.3;%費洛蒙揮發係數
Fmole=0.1;
%%
first=randperm(CAPITAL);
for i =1:CAPITAL
    if i == CAPITAL
        break
    else
        F(first(i),first(i+1))=  F(first(i),first(i+1))+Fmole;
    end
end
firstant=first;
anttwo=[];

for run =1:PP
    antdestion=[];
    antskechle=[];
    for l =1:antp
        for j =1:CAPITAL
            if j == 1
                cap1=1:CAPITAL;
                transform=randperm(length(cap1),1);
                cap1(transform)=[];
                anttwo=[transform];
            else
                
                if rand()<F1%找費洛蒙最大者
                    bigF=F(anttwo(j-1),cap1);
                    delete=find(cap1==cap1(find(bigF==max(bigF),1)));
                    anttwo=[ anttwo,cap1(delete)];
                    cap1(delete)=[];
                else%輪盤法(望大)                   
                    char=F(j-1,cap1);
                    for s =1:length(char)
                        if char(s)==0
                            char=char+Fmole.*0.01;
                        end
                    end
                    mo=1./char;
                    mO=mo./sum(mo);
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
        %單隻走完做局部更新套用公式(17)
        for k = 1:CAPITAL
            
            if k==1
                destionA=0;
                F(anttwo(k),anttwo(k))=(1-HOTF).*1+ F(anttwo(k),anttwo(k));
            else
                destionA= destionA+destion(anttwo(k-1),anttwo(k));
                F(anttwo(k-1),anttwo(k))=(1-HOTF).*1+ F(anttwo(k-1),anttwo(k));
            end
        end
        antdestion=[antdestion; destionA];
        antskechle=[antskechle; anttwo];
    end
    %全部走完做全域更新(挑最短距離並增加路徑的費洛蒙)
    best1=find(antdestion==(min(antdestion)),1);
    best= antskechle(best1,:);
    for m =1:CAPITAL
        if m==1
            F( best(m), best(m)) = (1-HOTF).* F( best(m), best(m))+ F( best(m), best(m));
        else
            F( best(m-1), best(m))=(1-HOTF).* F( best(m-1), best(m))+ F( best(m-1), best(m));
        end
    end
end
best1=find(antdestion==(min(antdestion)),1)
antdestion(best1)
antskechle(best1,:)



%迭代數判斷終止演化
%產生最佳路徑
%20220304  A B  公式計算修改 初始起點無費洛蒙濃度
 









