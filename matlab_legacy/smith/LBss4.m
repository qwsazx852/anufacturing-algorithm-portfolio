function SS = LBss4(asb,asb2,RR); %計算適應值(選拆利潤(拆解成本最大)碳足跡(拆解碳足跡最大)目標式)
% %% 拆裝時間
% RR=[9	7	1	6	5	12	2	13	15	10	3	16	17	8	4	11	18	14]
% asb=[18]
% asb2=[1]
add=0;
ans=[];
for run =1:2
    add=0;
    a=[];
    if run==2
        asb=asb2;
    end
    for i =length(asb)
        a=[a,find(RR==asb(i))];
    end
    d=RR(max(a):end);
    %% 選拆後利潤
    if run ==1
        for j =1:length(d)
            add=add+d(j).*10;

        end
    else
        for c =1:length(d)
            add=add+d(c).*5;

        end
    end

    ans=[ans,add];
end

w1=rand;
w2=1-w1;
SS=w1.* ans(1)./w2.* ans(2);