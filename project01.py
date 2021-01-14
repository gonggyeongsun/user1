import pymysql
from prettytable import PrettyTable

con = pymysql.connect(host ="127.0.0.1", user = 'root', password ="", port=13306, db="mydb", charset="utf8")
cursor = con.cursor()
   
def search_user(user_id : str, user_pwd : str) :
    selectSql = '''SELECT id, name, email, pwd, created_at FROM Member WHERE id = %s AND pwd = %s'''
    cursor.execute(selectSql,(user_id, user_pwd))
    rows = cursor.fetchall()

    if (user_id != rows[0][0] or user_pwd != rows[0][3]) :
        raise IndexError
    elif user_id == 'admin' and user_pwd == 'admin1234':
        print("관리자입니다. 관리자 로그인 메뉴로 이동하세요.")
    else :
        print("{0}님 로그인에 성공 하셨습니다.".format(user_id))
        UserMenu()

def search_mn(mn_id : str, mn_pwd : str) :
    mnselectSql = "SELECT id, name, email, pwd, created_at FROM Member WHERE id = %s AND pwd = %s"
    cursor.execute(mnselectSql,(mn_id, mn_pwd))
    rows = cursor.fetchall()

    if rows[0][0] == 'admin' and rows[0][3] == 'admin1234':
        print("관리자님 로그인에 성공하셨습니다.")
        MnMenu()
    else :
        print("관리자가 아닙니다.")

def join(join_id : str, join_pwd : str, join_name : str, join_email : str) :
    insertSql = '''INSERT INTO Member(id, name, email, pwd, created_at) VALUES (%s, %s, %s, %s, NOW())'''
    cursor.execute(insertSql,(join_id, join_name, join_email, join_pwd))
    con.commit()
    print("ID : {0} \nNAME : {1}\nEMAIL: {2}\n가입이 완료 되었습니다.".format(join_id, join_name, join_email))

def OrderItem(orderid, orderqty):

     selectSql = "SELECT id, product_name, product_price, product_qty FROM Item WHERE id = %s"
     cursor.execute(selectSql,(orderid))
     rows = cursor.fetchall()
     
     orderprice = str(int(rows[0][2]) * int(orderqty))
     insertSql = """INSERT INTO ItemOrder(member_id, item_id, order_qty, order_price, created_at) VALUES(%s, %s, %s, %s, NOW())"""
     cursor.execute(insertSql,(user_id ,orderid, orderqty, orderprice))
     con.commit()
    
     updateSql = "UPDATE Item SET product_qty = %s WHERE id = %s"
     orderqty1 = str(int(rows[0][3]) - int(orderqty))
     cursor.execute(updateSql,(orderqty1, orderid))
     con.commit()
     print("상품 - ID : {0}  NAME : {1}  QUANTITY : {2} 주문이 완료 되었습니다. \n총 가격은 {3}원입니다.".format(rows[0][0], rows[0][1], orderqty, orderprice))
     
def menu_list():
    table = PrettyTable()
    table.field_names=['상품 ID', '상품 이름', '상품 가격', '남은 수량']
    selectSql = "SELECT id, product_name, product_price, product_qty FROM Item WHERE product_qty > '0'"
    cursor.execute(selectSql)
    rows = cursor.fetchall()
    if len(rows) == 0 :
        print("주문 가능한 상품이 없습니다.")        
    else:
        print('-'*50)
        print(" < 주문 가능한 상품 목록 > ")
        print('-'*50)
        if len(rows) > 0:
            for row in rows : 
                table.add_row([row[0], row[1], row[2], row[3]])
            print(table)
        print("주문 하실 상품의 id와 개수를 적어 주세요.")
        orderid = input(" - 상품 ID : ")
        orderqty = input(" - 주문 수량 : ")
        OrderItem(orderid, orderqty)

def OrderProduct():

    table = PrettyTable()
    table.field_names=['주문 번호', '회원 ID', '상품 ID', '주문 수량', '주문 가격', '주문 날짜']
    selectSql = "SELECT * FROM ItemOrder WHERE member_id = %s"
    cursor.execute(selectSql,(user_id, ))
    rows = cursor.fetchall()
    print('-'*80)
    print(' < 주문한 상품 목록 > ')
    print('-'*80)
    if len(rows) > 0 :
        for row in rows :
            table.add_row([row[0], row[1], row[2], row[3], row[4], row[5]])
    print(table)

def myinfo() : 
    table = PrettyTable()
    table.field_names=['ID', '이름', '이메일', '비밀번호', '가입 날짜']
    selectSql = "SELECT * FROM Member WHERE id = %s"
    cursor.execute(selectSql,(user_id))
    rows = cursor.fetchall()
    if len(rows) > 0 :
        for row in rows : 
            table.add_row([row[0], row[1], row[2], row[3], row[4]])
        print(table)

def UpdateUSer(updatenum : int, updateinfo : str) :
    if updatenum == 1 :
        updateSql = "UPDATE Member SET name=%s WHERE id=%s"
        cursor.execute(updateSql,(updateinfo, user_id))
    elif updatenum == 2 :
        updateSql = "UPDATE Member SET pwd=%s WHERE id=%s"
        cursor.execute(updateSql,(updateinfo, user_id))
    elif updatenum == 3 :
        updateSql = "UPDATE Member SET email=%s WHERE id=%s"
        cursor.execute(updateSql,(updateinfo, user_id))
    else : 
        print("메뉴에 있는 번호를 입력하세요.")    
    con.commit()
    print(" 변경이 완료 되었습니다. ")

def DeleteInfo() :
    deleteSql = "DELETE FROM Member WHERE id = %s"
    cursor.execute(deleteSql,(user_id))
    deleteSql = "DELETE FROM ItemOrder WHERE member_id = %s"
    cursor.execute(deleteSql,(user_id))
    con.commit()
    print(" 회원 탈퇴가 완료 되었습니다. ")

def AllUser():
    table = PrettyTable()
    table.field_names=['ID', '이름', '이메일', '비밀번호', '가입 날짜']
    selectSql = "SELECT * FROM Member"
    cursor.execute(selectSql)
    rows = cursor.fetchall()
    if len(rows) > 0 :
        for row in rows : 
            table.add_row([row[0], row[1], row[2], row[3], row[4]])
        print(table)

def AllOrder():
    table = PrettyTable()
    table.field_names=['주문 번호', '회원 ID', '상품 ID', '주문 수량', '가격', '주문 날짜']
    selectSql = "SELECT * FROM ItemOrder"
    cursor.execute(selectSql)
    rows = cursor.fetchall()
    if len(rows) > 0 :
        for row in rows : 
                table.add_row([row[0], row[1], row[2], row[3], row[4], row[5]])
        print(table)

def AddProduct(product : list):
    insertSql = "INSERT INTO Item(id, product_name, product_price, product_qty, created_at) VALUES(%s, %s, %s, %s, NOW()) "
    cursor.execute(insertSql,(product[0], product[1], product[0], product[0]))
    con.commit()
    print("ID : {0} \nNAME : {1}\nPRICE: {2}\nQUANTITY : {3} \n상품 등록이 완료 되었습니다.".format(product[0], product[1], product[2], product[3]))

def idOrder(orderid):
    table = PrettyTable()
    table.field_names=['주문 번호', '회원 ID', '상품 ID', '주문 수량', '가격', '주문 날짜']
    selectSql = "SELECT * FROM ItemOrder WHERE member_id = %s"
    cursor.execute(selectSql,(orderid))
    rows = cursor.fetchall()
    print(" {0}님이 주문한 상품 목록입니다. ".format(orderid))
    if len(rows) > 0 :
        for row in rows : 
                table.add_row([row[0], row[1], row[2], row[3], row[4], row[5]])
        print(table)

def WeekUser() :
    table = PrettyTable()
    table.field_names=['회원 ID', '합계 금액']
    selectSql ="""SELECT member_id, SUM(order_price)as sum FROM ItemOrder  
    WHERE created_at BETWEEN DATE_ADD(NOW(), INTERVAL -7 DAY) AND NOW() GROUP BY member_id ORDER BY sum DESC"""
    cursor.execute(selectSql)
    rows = cursor.fetchall()
    print('-'*50)
    print("최근 일주일간 많은 금액을 주문한 사용자 랭킹")
    print('-'*50)
    if len(rows) > 0 :
        for row in rows : 
                table.add_row([row[0], row[1]])
        print(table)
    print("최근 일주일간 가장 많은 금액을 주문한 사용자는 {0}님입니다. \n총 주문 금액 : {1} ".format(rows[0][0], int(rows[0][1])))

def MaxUser(user_month) :
    table = PrettyTable()
    table.field_names=['주문 달', '회원 ID', '합계 금액']
    selectSql = """SELECT MONTH(created_at)as month, member_id, SUM(order_price)as sum FROM ItemOrder 
    GROUP BY month, member_id HAVING month = %s ORDER BY sum DESC"""
    cursor.execute(selectSql,(user_month))
    rows = cursor.fetchall()
    print('-'*50)
    print("{0}월에 많은 금액을 주문한 사용자 랭킹".format(user_month))
    print('-'*50)
    if len(rows) > 0 :
        for row in rows : 
                table.add_row([row[0], row[1], row[2]])
        print(table)
    print("{0}월에 가장 많은 금액을 주문한 사용자는 {1}님입니다. \n총 주문 금액 : {2} ".format(user_month, rows[0][1], int(rows[0][2])))

def WeekProduct():
    table = PrettyTable()
    table.field_names=['아이템 ID', '합계 수량']
    selectSql = """SELECT item_id, SUM(order_qty)as sum FROM ItemOrder 
    WHERE created_at BETWEEN DATE_ADD(NOW(), INTERVAL -7 DAY) AND NOW() GROUP BY item_id ORDER BY sum DESC"""
    cursor.execute(selectSql)
    rows = cursor.fetchall()
    if len(rows) > 0 :
        for row in rows : 
                table.add_row([row[0], row[1]])
        print(table)
    print("최근 일주일간 가장 많이 팔린 상품은 ITEM_ID : {0} {1}개가 팔렸습니다.".format(rows[0][0], int(rows[0][1])))

def MaxItem(month) : 
    table = PrettyTable()
    table.field_names=['주문 달', '아이템 ID', '합계 수량']
    selectSql = """SELECT MONTH(created_at)as month, item_id, SUM(order_qty)as sum FROM ItemOrder 
    GROUP BY month, item_id HAVING month = %s ORDER BY sum DESC"""
    cursor.execute(selectSql,(month))
    rows = cursor.fetchall()
    print('-'*50)
    print("{0}월 주문 상품 랭킹".format(month))
    print('-'*50)
    if len(rows) > 0 :
        for row in rows : 
                table.add_row([row[0], row[1], row[2]])
        print(table)
    print("{0}월에 가장 많이 팔린 상품은 ITEM_ID : {1}상품 {2}개가 팔렸습니다. ".format(month, rows[0][1], int(rows[0][2])))

def UserMenu():
        while True:
            print('-'*50)
            print(' < 사용자 메뉴 > ')
            print('-'*50)
            print('1. 주문 가능한 상품 목록 보기와 주문하기 \n2. 주문한 상품 목록 보기 \n3. 회원 정보 수정 \n4. 회원 탈퇴 \n5. 뒤로가기')
            user_menu = input("메뉴를 선택해 주세요. -> ")
            if user_menu == '1' : 
                menu_list()
            elif user_menu == '2' :
                OrderProduct()
            elif user_menu == '3' :
                print(" < 회원 정보 수정 > ")
                updatepwd = input(" - 비밀번호를 입력하세요 :")
                if(user_pwd==updatepwd) :
                    myinfo()  
                    updatenum = int(input("수정 할 정보를 선택하세요. \n1. 이름 \n2. 비밀번호 \n3. 이메일 \n --> "))
                    updateinfo = input("수정된 정보를 입력하세요. : ")
                    UpdateUSer(updatenum, updateinfo)
                else :
                    print("비밀번호가 틀렸습니다.")
            elif user_menu == '4' :
                question = input(" {0}님 회원 탈퇴 하시겠습니까?\n1. Yes \t2. NO \n --> ".format(user_id))
                if question == '1' : 
                    DeleteInfo()
                    break
                elif question == '2' :
                    print(" 회원 탈퇴 취소 ")
                    pass
                else :
                    print(" 잘못된 값입니다. ")
            elif user_menu == '5' : 
                break
            else : 
                print("메뉴에 있는 번호를 입력해 주세요.")

def MnMenu() : 
    try:
        while True:
            print('-'*50)
            print(' < 관리자 메뉴 > ')
            print('-'*50)
            print('1. 전체 회원 목록 조회 \n2. 전체 주문 목록 조회 \n3. 회원별 주문 목록 조회 \n4. 상품 추가 하기 \n5. 주/월별로 가장 많은 금액을 주문한 사용자 \n6. 주/월별로 가장 많이 주문된 상품 목록 조회 \n7. 뒤로가기')
            mn_menu = input("메뉴를 선택해 주세요. -> ")
            if mn_menu == '1' :
                print('-'*50)
                print (" < 전체 회원 목록 > ")
                print('-'*50)
                AllUser()
            elif mn_menu == '2' :
                print('-'*50)
                print (" < 전체 주문 목록 > ")
                print('-'*50)
                AllOrder()
            elif mn_menu == '3' :
                print('-'*50)
                print(" < 회원별 주문 목록 조회 > ")
                print('-'*50)
                orderid = input("조회할 회원의 id를 입력해주세요. \n- 아이디 : ")
                idOrder(orderid)
            elif mn_menu == '4' :
                while True: 
                    print('-'*50)
                    print (" < 상품 추가 > ")
                    print('-'*50)
                    product = input("상품의 정보를 입력해 주세요 \n[상품ID 상품이름 상품가격 상품개수]\n(공백으로 구별해 주세요.) \n ->")
                    product = list(product.split())
                    if len(product) != 4:
                        print("잘 못 입력 했습니다. 다시 입력해주세요.\n")
                    else:
                        AddProduct(product)
                        break
            elif mn_menu == '5' :
                mm = input("1. 주별 목록\n2. 월별 목록 \n 선택해주세요 -> ")
                if mm == '1' :
                    print('-'*50)
                    print(" 최근 일주일간 많은 금액을 주문한 사용자 랭킹 ")
                    print('-'*50)
                    WeekUser() 
                elif mm == '2' :
                    print('-'*50)
                    print("월별로 가장 많은 금액을 주문한 사용자")
                    print('-'*50)
                    user_month = input("조회하고 싶은 달을 선택해 주세요.(1 ~ 12) : ")
                    MaxUser(user_month)
                else : 
                    print(" 메뉴에 있는 번호를 선택하세요. ")
            elif mn_menu == '6':
                ww = input("1. 주별 목록\n2. 월별 목록 \n 선택해주세요 -> ")
                if ww == '1' :
                    print('-'*50)
                    print(" 최근 일주일간 많이 주문 된 상품 랭킹 ")
                    print('-'*50)
                    WeekProduct() 
                elif ww == '2' :
                    print('-'*50)
                    print("월별로 가장 많이 주문 된 상품 조회")
                    print('-'*50)
                    month = input("조회하고 싶은 달을 선택해 주세요.(1 ~ 12) : ")
                    MaxItem(month)    
            elif mn_menu == '7' :
                break
            else :
                print(" 메뉴에 있는 번호를 선택하세요. ")  
    except IndexError :          
        print(" 목록이 존재하지 않습니다. ")   

def main(): 
    while True:
        try:
            print('-'*50)
            print(' < 쇼핑몰 메인 화면 > ')
            print('-'*50)
            print('1. 회원 로그인 \n2. 관리자 로그인 \n3. 회원 가입 \n4. 종료')
            print('-'*50)
            log_menu = int(input("메뉴를 선택해 주세요. -> "))

            if log_menu == 1 :
                print('-'*50)
                print(" < 회원 로그인 화면 >") 
                print('-'*50)
                print(" | 아이디와 비밀번호를 입력해주세요. | ")
                global user_id
                global user_pwd
                user_id = input("- 아이디 : ")
                user_pwd = input("- 비밀번호 : ")
                search_user(user_id, user_pwd)

            elif log_menu == 2 :
                print('-'*50)
                print(" < 관리자 로그인 화면 > ") 
                print('-'*50)
                print(" 아이디와 비밀번호를 입력해주세요. ")
                mn_id = input(" - 아이디 : ")
                mn_pwd = input(" - 비밀번호 : ")
                search_mn(mn_id, mn_pwd)
            
            elif log_menu == 3 :
                print("-"*50)
                print(" < 가입 정보를 입력해주세요. > ")
                join_id = input("ID : ")
                join_pwd = input("PASSWORD : ")
                join_name = input("NAME : ")
                join_email = input("EMAIL : ")
                join(join_id, join_pwd, join_name, join_email)
            
            elif log_menu == 4 :
                break
            
            else :
                print("메뉴에 있는 번호를 입력하세요.")

        except IndexError :
            print("잘못된 값입니다. 다시 확인하세요. Index")
            
        except ValueError : 
            print("잘못된 값입니다. 다시 확인하세요. Value")
        except pymysql.err.IntegrityError : 
            print("이미 존재하는 아이디입니다.")
        except pymysql.err.OperationalError:
            print("잘못된 값입니다. 다시 확인하세요.")

main()

