import csv
import copy #deepcopy
import pandas as pd
import time
import pulp

def input_element():#要素をリストとしてinput
    f=open('test.txt','r',encoding="utf-8")
    Pin=list(f.readline().split())
    Cin=list(f.readline().split())
    Din=list(f.readline().split())
    Tin=list(f.readline().split())
    Sin=list(f.readline().split())
    Rin=list(f.readline().split())
    Iin=list(f.readline().split())
    return Pin,Cin,Din,Tin,Sin,Rin,Iin
P,C,D,T,S,R,I=input_element()

timed2=[[0,1],[2,3],[4,5],[5,6],[6,7]]
timed3=[[0,1,2],[1,2,3],[4,5,6],[5,6,7]]

def keisan(P,D,T):#値の計算
    N=len(P)*len(D)*len(T)#前期/後期、曜日、時限
    plen=len(D)*len(T)
    dlen=len(T)
    return N,plen,dlen
N,plen,dlen=keisan(P,D,T)

# 右辺bの値によって格納場所を区別
keisuu0=[]
keisuu1=[]
keisuu2=[]
keisuu3=[]
keisuu4=[]

x=[]#有効範囲の指定用list
def keisuu01():
    #０行列
    all0=[]
    for n in range(N):
        all0.append(0)
    #１行列
    all1=[]
    for n in range(N):
        all1.append(1)
    #csvファイルopen
    filename='test.csv'
    with open(filename, encoding='utf8', newline='') as f:#csvファイルopen&listに格納
        header = next(csv.reader(f))
        csvreader = csv.reader(f)
        #0行列の作成
        m=0
        csvlist=[]#csvをlist化
        for i in csvreader:
            m+=1#行数
            a=[]
            for j in i:#csv読み込んだ行のセル内容
                a.append(j)
            csvlist.append(a)
        all0=all0*m#P*D*Tの０行列をcsvの行分増やす
        all1=all1*m
        csvline=m
        return all0,all1,csvline,csvlist
all0,all1,csvline,csvlist=keisuu01()
# print(csvline)
# print(len(all0))



def tyouhuku():#重複なしの授業の割り当て(前期のみ)
    # 教員重複制約
    for i in I:
        irow=[]
        r=0
        for j in csvlist:
            if j[0]==i:
                irow.append(r)
            r+=1
        for p in range(len(P)):
            for d in range(len(D)):
                for t in range(len(T)):
                    list=copy.deepcopy(all0)
                    for k in irow:
                        m=k*N + p*plen + d*dlen + t
                        if m not in x:
                            x.append(m)
                        # print(m,end=',')
                        list[m]=1
                    # print()
                    keisuu1.append(list)

    # 授業重複制約
    for c in range(4):
        crow=[]#csvの条件に合う行の番号を保存
        r=0#行番号カウンタ
        for i in csvlist:
            if i[2]==C[c]:#特定のクラスの授業のみをpickup
                crow.append(r)
            r+=1
        #↑クラスが同じ行番号の抽出完了↑


        # Σs Xspdt = 1 一つの時限に一つの科目のみ
        for p in range(len(P)):
            for d in range(len(D)):
                for t in range(len(T)):
                    list=copy.deepcopy(all0)
                    for i in range(len(crow)):
                        m=crow[i]*N + p*plen + d*dlen + t
                        if m not in x:
                            x.append(m)
                        # print(m,end=',')
                        list[m]=1
                    # print()
                    keisuu1.append(list)
tyouhuku()

def wariate():
    for c in range(4):
        # print(C[c])
        crow=[]#csvの条件に合う行の番号を保存
        r=0#行番号カウンタ
        for i in csvlist:
            if i[2]==C[0]:#特定のクラスの授業のみをpickup
                crow.append(r)
            r+=1

        for i in crow:#対応したクラスの科目行を一つ抽出
            # if csvlist[i][7]=='通':   #通年授業のみ適応
            #     # ΣdΣt Xspdt = 1
            #     if csvlist[i][3]=='1':
            # print(csvlist[i][1],csvlist[i][0])
            for p in range(len(P)):
                list=copy.deepcopy(all0)
                for d in range(len(D)):
                    for t in range(len(T)):
                        m=i*N + p*plen + d*dlen + t
                        # print(m,end=',')
                        if m not in x:
                            x.append(m)
                        list[m]=1
                    # print()
                keisuu1.append(list)
                # print()
                #
                # # ΣdΣt Xspdt = 2
                # if csvlist[i][3]=='2':
                #     print(csvlist[i][1],csvlist[i][0])
                #     for p in range(len(P)):
                #         list=copy.deepcopy(all0)
                #         for d in range(len(D)):
                #             for t in range(len(T)):
                #                 m=i*N + p*plen + d*dlen + t
                #                 print(m,end=',')
                #                 if m not in x:
                #                     x.append(m)
                #                 # print(m,end=',')
                #                 list[m]=1
                #             # print()
                #         keisuu2.append(list)
                #         print()
                #
                # # ΣdΣt Xspdt = 3
                # if csvlist[i][3]=='3':
                #     print(csvlist[i][1],csvlist[i][0])
                #     for p in range(len(P)):
                #         list=copy.deepcopy(all0)
                #         for d in range(len(D)):
                #             for t in range(len(T)):
                #                 m=i*N + p*plen + d*dlen + t
                #                 print(m,end=',')
                #                 if m not in x:
                #                     x.append(m)
                #                 # print(m,end=',')
                #                 list[m]=1
                #             # print()
                #         keisuu3.append(list)
                #         print()
                #
                # # ΣdΣt Xspdt = 4
                # if csvlist[i][3]=='4':
                #     print(csvlist[i][1],csvlist[i][0])
                #     for p in range(len(P)):
                #         list=copy.deepcopy(all0)
                #         for d in range(len(D)):
                #             for t in range(len(T)):
                #                 m=i*N + p*plen + d*dlen + t
                #                 print(m,end=',')
                #                 if m not in x:
                #                     x.append(m)
                #                 # print(m,end=',')
                #                 list[m]=1
                #             # print()
                #         keisuu4.append(list)
                #         print()


# --------------
#             # 半期科目(前期後期どちらでもいい)
#             if csvlist[i][7]=='半':
#                 # ΣdΣt Xspdt = 1
#                 if csvlist[i][3]=='1':
#                     print(csvlist[i][1],csvlist[i][0])
#                     list=copy.deepcopy(all0)
#                     for p in range(len(P)):
#                         for d in range(len(D)):
#                             for t in range(len(T)):
#                                 m=i*N + p*plen + d*dlen + t
#                                 print(m,end=',')
#                                 if m not in x:
#                                     x.append(m)
#                                 # print(m,end=',')
#                                 list[m]=1
#                             # print()
#                     keisuu1.append(list)
#                     print()
#
#                 # ΣdΣt Xspdt = 2
#                 if csvlist[i][3]=='2':
#                     print(csvlist[i][1],csvlist[i][0])
#                     list=copy.deepcopy(all0)
#                     for p in range(len(P)):
#                         for d in range(len(D)):
#                             for t in range(len(T)):
#                                 m=i*N + p*plen + d*dlen + t
#                                 print(m,end=',')
#                                 if m not in x:
#                                     x.append(m)
#                                 # print(m,end=',')
#                                 list[m]=1
#                             # print()
#                     keisuu2.append(list)
#                     print()
#
#                 # ΣdΣt Xspdt = 3
#                 if csvlist[i][3]=='3':
#                     print(csvlist[i][1],csvlist[i][0])
#                     list=copy.deepcopy(all0)
#                     for p in range(len(P)):
#                         for d in range(len(D)):
#                             for t in range(len(T)):
#                                 m=i*N + p*plen + d*dlen + t
#                                 print(m,end=',')
#                                 if m not in x:
#                                     x.append(m)
#                                 # print(m,end=',')
#                                 list[m]=1
#                             # print()
#                     keisuu3.append(list)
#                     print()
#
#                 # ΣdΣt Xspdt = 4
#                 if csvlist[i][3]=='4':
#                     print(csvlist[i][1],csvlist[i][0])
#                     list=copy.deepcopy(all0)
#                     for p in range(len(P)):
#                         for d in range(len(D)):
#                             for t in range(len(T)):
#                                 m=i*N + p*plen + d*dlen + t
#                                 print(m,end=',')
#                                 if m not in x:
#                                     x.append(m)
#                                 # print(m,end=',')
#                                 list[m]=1
#                             # print()
#                     keisuu4.append(list)
#                     print()
#
# # -------------
#             # 前期科目
#             if csvlist[i][7]=='前':
#                 # ΣdΣt Xspdt = 1
#                 if csvlist[i][3]=='1':
#                     print(csvlist[i][1],csvlist[i][0])
#                     list=copy.deepcopy(all0)
#                     for d in range(len(D)):
#                         for t in range(len(T)):
#                             m=i*N + 0*plen + d*dlen + t
#                             print(m,end=',')
#                             if m not in x:
#                                 x.append(m)
#                             # print(m,end=',')
#                             list[m]=1
#                             # print()
#                     keisuu1.append(list)
#                     print()
#
#                 # ΣdΣt Xspdt = 2
#                 if csvlist[i][3]=='2':
#                     print(csvlist[i][1],csvlist[i][0])
#                     list=copy.deepcopy(all0)
#                     for d in range(len(D)):
#                         for t in range(len(T)):
#                             m=i*N + 0*plen + d*dlen + t
#                             print(m,end=',')
#                             if m not in x:
#                                 x.append(m)
#                             # print(m,end=',')
#                             list[m]=1
#                         # print()
#                     keisuu2.append(list)
#                     print()
#
#                 if csvlist[i][3]=='3':
#                     print(csvlist[i][1],csvlist[i][0])
#                     list=copy.deepcopy(all0)
#                     for d in range(len(D)):
#                         for t in range(len(T)):
#                             m=i*N + 0*plen + d*dlen + t
#                             print(m,end=',')
#                             if m not in x:
#                                 x.append(m)
#                             # print(m,end=',')
#                             list[m]=1
#                         # print()
#                     keisuu3.append(list)
#                     print()
#
#                 if csvlist[i][3]=='4':
#                     print(csvlist[i][1],csvlist[i][0])
#                     list=copy.deepcopy(all0)
#                     for d in range(len(D)):
#                         for t in range(len(T)):
#                             m=i*N + 0*plen + d*dlen + t
#                             print(m,end=',')
#                             if m not in x:
#                                 x.append(m)
#                             # print(m,end=',')
#                             list[m]=1
#                         # print()
#                     keisuu4.append(list)
#                     print()
#
# # -------------
#             # 後期科目
#             if csvlist[i][7]=='後':
#                 # ΣdΣt Xspdt = 1
#                 if csvlist[i][3]=='1':
#                     print(csvlist[i][1],csvlist[i][0])
#                     list=copy.deepcopy(all0)
#                     for d in range(len(D)):
#                         for t in range(len(T)):
#                             m=i*N + 1*plen + d*dlen + t
#                             print(m,end=',')
#                             if m not in x:
#                                 x.append(m)
#                             # print(m,end=',')
#                             list[m]=1
#                             # print()
#                     keisuu1.append(list)
#                     print()
#
#                 # ΣdΣt Xspdt = 2
#                 if csvlist[i][3]=='2':
#                     print(csvlist[i][1],csvlist[i][0])
#                     list=copy.deepcopy(all0)
#                     for d in range(len(D)):
#                         for t in range(len(T)):
#                             m=i*N + 1*plen + d*dlen + t
#                             print(m,end=',')
#                             if m not in x:
#                                 x.append(m)
#                             # print(m,end=',')
#                             list[m]=1
#                         # print()
#                     keisuu2.append(list)
#                     print()
#
#                 if csvlist[i][3]=='3':
#                     print(csvlist[i][1],csvlist[i][0])
#                     list=copy.deepcopy(all0)
#                     for d in range(len(D)):
#                         for t in range(len(T)):
#                             m=i*N + 1*plen + d*dlen + t
#                             print(m,end=',')
#                             if m not in x:
#                                 x.append(m)
#                             # print(m,end=',')
#                             list[m]=1
#                         # print()
#                     keisuu3.append(list)
#                     print()
#
#                 if csvlist[i][3]=='4':
#                     print(csvlist[i][1],csvlist[i][0])
#                     list=copy.deepcopy(all0)
#                     for d in range(len(D)):
#                         for t in range(len(T)):
#                             m=i*N + 1*plen + d*dlen + t
#                             print(m,end=',')
#                             if m not in x:
#                                 x.append(m)
#                             # print(m,end=',')
#                             list[m]=1
#                         # print()
#                     keisuu4.append(list)
#                     print()

wariate()

def renzoku():
    for c in range(4):
        crow=[]#csvの条件に合う行の番号を保存
        r=0#行番号カウンタ
        for i in csvlist:
            if i[2]==C[c]:#特定のクラスの授業のみをpickup
                crow.append(r)
            r+=1

        for i in crow:
            # 連続時間制約
            if csvlist[i][3] == '2':
                for p in range(len(P)):
                    for d in range(len(D)):
                        for t in timed2:
                            list=copy.deepcopy(all0)
                            m=i*N + p*plen + d*dlen + t[0]
                            if m not in x:
                                x.append(m)
                            list[m]=1
                            m=i*N + p*plen + d*dlen + t[1]
                            if m not in x:
                                x.append(m)
                            list[m]=-1
                            keisuu0.append(list)

# renzoku()

def scale():
    # 範囲指定 all1→0
    for i in range(len(x)):
        m=x[i]
        all1[m]=0

    for c in range(4):
        crow=[]#csvの条件に合う行の番号を保存
        r=0#行番号カウンタ
        for i in csvlist:
            if i[2]==C[c]:#特定のクラスの授業のみをpickup
                crow.append(r)
            r+=1
        #↑クラスが同じ行番号の抽出完了↑
        for i in range(len(crow)):
            for p in range(len(P)):
                for d in range(len(D)):
                    for t in range(len(T)):
                        #火曜日7,8限入れない
                        if d==1 and t==6:
                            m=crow[i]*N + p*plen + d*dlen + t
                            all1[m]=1
                        if d==1 and t==7:
                            m=crow[i]*N + p*plen + d*dlen + t
                            all1[m]=1
                        # 一年生水曜日7,8限入れない(LHRのため)(後に2年も追加予定)
                        if 0<=c<=3 and d==2 and t==6:
                            m=crow[i]*N + p*plen + d*dlen + t
                            all1[m]=1
                        if 0<=c<=3 and d==2 and t==7:
                            m=crow[i]*N + p*plen + d*dlen + t
                            all1[m]=1
    # print(all1)
scale()

#csvlistから教員、クラスデータ取得
def csv_isc():

    csv_instructor=[]
    csv_subject=[]
    csv_class=[]
    for i in range(len(csvlist)):
        csv_instructor.append(csvlist[i][0])
        csv_subject.append(csvlist[i][1])
        csv_class.append(csvlist[i][2])
    return csv_instructor,csv_subject,csv_class
csv_instructor,csv_subject,csv_class=csv_isc()


# ------------------------------------------------------------------
#pulpに格納＆計算（integerprogramming整数計画法）
def keisan_pulp():
    start=time.time()
    # (1) 問題を定義
    problem = pulp.LpProblem( "test", pulp.LpMaximize )
    # (2) 変数を定義
    x = [ pulp.LpVariable( 'x_{}'.format( i ), cat=pulp.LpBinary ) for i in range(len(all0)) ]
    # (3) 係数をセット
    c =[]
    for i in range(len(all0)):
        c.append(1)
    a = []
    b=[0,1,2,3,4]  # 制約不等式右辺
    # (4) 目的関数をセット
    problem += pulp.lpDot( c, x )
    # (5) 制約条件をセット
    for k in b:
        if k==0:
            a=all1
            problem += pulp.lpDot( a, x ) <= k
            for l in keisuu0:
                problem += pulp.lpDot( l, x ) <= k
        if k==1:
            for l in keisuu1:
                problem += pulp.lpDot( l, x ) <= k
        if k==2:
            for l in keisuu2:
                problem += pulp.lpDot( l, x ) <= k
        if k==3:
            for l in keisuu3:
                problem += pulp.lpDot( l, x ) <= k
        if k==4:
            for l in keisuu4:
                problem += pulp.lpDot( l, x ) <= k

    # (6) 解く
    result = problem.solve()
    end=time.time() - start
    # 結果を出力
    # print('objective value: {}'.format(pulp.value(problem.objective)))
    # print('solution')
    x_ans=[]
    for i in range(len(x)):
        # print('x_{} = {}'.format( i, pulp.value(x[i]) ))
        x_ans.append(pulp.value(x[i]))
    # print ("elapsed_time:{0}".format(end) + "[sec]")
    # print(x_ans)
    return x_ans
ans=keisan_pulp()


#ansを取り込んで、時間割を作成
dis_ans=[]
cnt=0
def display():
    global cnt
    index=[i for i, x in enumerate(ans) if x == 1]#ansの1地点のindex取得
    # print(len(index))
    # print(index)
    for j in index:
        spdtc=[]
        s=j//N#ある教員があるクラスに実施する科目
        p=j%N//plen
        d=j%plen//dlen
        t=j%dlen
        spdtc.append(s)
        spdtc.append(p)
        spdtc.append(d)
        spdtc.append(t)
        Class=csvlist[s][2]
        c=C.index(Class)
        spdtc.append(c)
        # print(spdtc,end=' ')
        dis_ans.append(spdtc)

    #spdtcをp,c,d,tを基準にソート
    df = pd.DataFrame(dis_ans, columns=['s','p','d','t','c'])
    pandas=df.sort_values(['p','c','d','t'])
    sort_spdtc=pandas.values.tolist()
    # print(sort_spdtc)

    pdis=0
    cdis=0
    ddis=0
    tdis=0
    sdis=0
    print(P[pdis],'期')
    print(' ','クラス',C[cdis])
    print('  ',D[ddis],'曜日')
    for k in range(len(sort_spdtc)):
        num=index[k]
        spdtc=sort_spdtc[k]
        sin=spdtc[0]
        pin=spdtc[1]
        din=spdtc[2]
        tin=spdtc[3]
        cin=spdtc[4]
        if pin!=pdis:
            print(P[pin],'期')
        if cin!=cdis:
            print(' ','クラス',C[cin])
            cnt=0
        if din!=ddis:
            print('  ',D[din],'曜日')
        print(cnt,'   ',T[tin],'限目',end='=>')
        print(csv_subject[sin],'(',csv_instructor[sin],')')
        cdis=cin
        sdis=sin
        ddis=din
        pdis=pin
        cnt+=1
    return
display()

        # p
        #     c
        #         d
        #             t,s,i
