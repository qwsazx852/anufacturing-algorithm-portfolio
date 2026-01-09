function a = LBb222(n,fxm_ans,a,b,Or,T1,T22,PP,mutation) %mutation 隨機兩點交換突變法
c=[];
mtimes=fix(n.*0.9);
for i = 1:nnz(b)
    q=rand();
    if q<mutation
        for j =1:mtimes
            c=fxm_ans{i};
            p=round(rand()*(n-1)+1,0);
            p1=round(rand()*(n-1)+1,0);
            while p==p1
                p1=round(rand()*(n-1)+1,0);
            end
            d=c(p);
            c(p)=c(p1);
            c(p1)=d;
            y = LBb2(c,n,Or);
            if y==2
                c = LBrr1(Or,n,c);
            end
        end
        fxm_ans{i}=c;
        %              b(i) =LBss1(GCT,Information,a(i,:))%%測試用
    end
end
a=fxm_ans;
  