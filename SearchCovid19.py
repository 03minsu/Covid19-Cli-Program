import csv
import pymysql
import matplotlib.pyplot as plt

conn = pymysql.connect(host='localhost', user='root', password='123456', db='covid19', charset='utf8')
curs = conn.cursor()

while True:

    print("*"*35,
    "\n(1) 서울 지역별 전체 확진자 수", 
    "\n(2) 특정 날짜 서울 전체 확진자 수",  
    "\n(3) n번째 확진자 정보 검색",  
    "\n(4) 특정 날짜 특정 지역 확진자 수",  
    "\n(5) 기타 검색", 
    "\n(q) EXIT")
    print("*"*35)

    trace=input('입력 : ')
    if trace=='q':
        print("프로그램 종료")
        break

    if trace == '1':
        place = input("\n지역 검색(구): ")
        sql = "select count(no) from covid19 where place='{0}'".format(place)
        curs.execute(sql)
        row = curs.fetchone()
        print("\n   {0} 에서 발생한 확진자 수는 총 {1} 명 입니다. \n  * 최초 발병일로부터 2021/04/04 기간 내 검색입니다. * \n".format(place,row[0]))
    elif trace == '2':
        print(" \n*** 입력 예: 20200326 *** ")
        print("\n2020/01/24 ~ 2021/04/04 사이 기간 내 검색입니다.")
        startDate = input("\n 검색 시작 날짜 입력 : ")
        endDate = input("\n 검색 종료 날짜 입력 : ")
        # 날짜 사이에 - 넣는 부분

        l1 = startDate[0:4]
        m1 = startDate[4:6]    
        r1 = startDate[6:8]

        l2 = endDate[0:4]
        m2 = endDate[4:6]    
        r2 = endDate[6:8]

        sql = "select count(no) from covid19 where infecD >= '{0}-{1}-{2}' and infecD <= '{3}-{4}-{5}'".format(l1,m1,r1,l2,m2,r2)
        curs.execute(sql)
        row = curs.fetchone()
        print("\n입력하신 기간 내 서울 확진자 수는 총 {0} 명 입니다. \n".format(row[0]))
    elif trace =='3':
        print("\n검색하실 확진자 번호를 입력하시면 관련 정보가 출력됩니다.")
        N = input("\n 입력 : ")
        sql="select * from covid19 where no ='{0}'".format(N)
        curs.execute(sql)
        row = curs.fetchone()
        print("\n{0} 번 확진자 정보입니다.\n확진일 : {1}\n거주지역 : {2}\n해외 이력 : {3}\n감염 경로 : {4}\n 상태 : {5}\n".format(row[0],row[1],row[2],row[3],row[4],row[5]))
        continue
    elif trace =='4':
        print(" \n*** 입력 예: 20200326 *** ")
        print("\n2020/01/24 ~ 2021/04/04 사이 기간 내 검색입니다.")
        startDate = input("\n 검색 시작 날짜 입력 : ")
        endDate = input("\n 검색 종료 날짜 입력 : ")
        # 날짜 사이에 - 넣는 부분

        l1 = startDate[0:4]
        m1 = startDate[4:6]    
        r1 = startDate[6:8]

        l2 = endDate[0:4]
        m2 = endDate[4:6]    
        r2 = endDate[6:8]

        place = input("\n지역 검색(구): ")
        sql="select count(no) from covid19 where infecD >= '{0}-{1}-{2}' and infecD <= '{3}-{4}-{5}' and place = '{6}'".format(l1,m1,r1,l2,m2,r2,place)
        curs.execute(sql)
        row = curs.fetchone()
        print("\n기간 내 {0} 지역 확진자는 총 {1} 명 입니다.\n".format(place,row[0]))
        continue
    elif trace =='5':
        chose = input("(1) 해외 유입 환자 통계 \n(2) 퇴원/사망 환자 통계  \n(3) 월별 확진자 통계 \n입력 : ")
        if chose == '1':
            sql = "select trv,count(trv) from covid19 group by trv having trv not like('') or trv not like('%%') order by count(trv) desc"
            curs.execute(sql)
            rows = curs.fetchall()
            for row in rows:
                print("\n",row[0],row[1],"명",end="\n")
            continue
        elif chose == '2':
            sql = "select replace(state,'','입원'), count(state) from covid19 group by state having state not like('')"
            curs.execute(sql)
            rows = curs.fetchall()
            for row in rows:
                print("\n",row[0],row[1],"명\n",end=" ")
            continue
        elif chose == '3':
            chose = input("(1) 2020년 통계 (2) 2021년 통계\n입력 :")
            if chose == '1':
                sql = "select date_format(infecD,'%y-%m') date,count(no) from covid19 group by date having date < 21"
                curs.execute(sql)
                rows = curs.fetchall()
                x = [1,2,3,4,5,6,7,8,9,10,11,12]
                y = []
                for row in rows:
                    y.append(row[1])
                plt.plot(x,y)
                plt.ylabel("Number of Infection")
                plt.xlabel("Month 2020")
                plt.grid(True)
                plt.show()
                continue
            elif chose == '2':
                sql = "select date_format(infecD,'%y-%m') date,count(no) from covid19 group by date having date = 21"
                curs.execute(sql)
                rows = curs.fetchall()
                x = [1,2,3,4]
                y = []
                for row in rows:
                    y.append(row[1])
                plt.plot(x,y)
                plt.ylabel("Number of Infection")
                plt.xlabel("Month 2021")
                plt.grid(True)
                plt.show()
                continue
    else:
        continue
conn.commit()
