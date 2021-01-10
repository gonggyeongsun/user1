import pymysql

conn = pymysql.connect(host ="127.0.0.1", user = 'root', password ="", port=13306, db="mydb", charset="utf8")
cursor = conn.cursor()

def show_list():
        selectSql='SELECT id, name, reg_date FROM member'
        cursor.execute(selectSql)
        rows = cursor.fetchall()
        for row in rows:
                print(row)

def search(search_id : str):
        selectSql1='SELECT id, name, reg_date FROM member WHERE id = %s'
        cursor.execute(selectSql1, (search_id, ))
        while True:
                rows = cursor.fetchone()
                if rows == None:
                        break
                print(rows)

def insert(insert_user : list) :
        insertSql = '''INSERT INTO member(id, name, pwd, reg_date) VALUES(%s, %s, %s, NOW())'''
        cursor.execute(insertSql,(insert_user[0], insert_user[1], insert_user[2]))
        conn.commit()

def delete(delete_user):
        deleteSql = 'DELETE FROM member WHERE id = %s'
        cursor.execute(deleteSql, (delete_user, ))
        conn.commit()

def main():
        while True:
                try:
                        print("[ 회원 관리 프로그램 ]")
                        print("1. 전체 회원 목록 보기")
                        print("2. 회원 검색")
                        print("3. 회원 등록")
                        print("4. 회원 삭제")
                        print("5. 종료")
                        cmd = int(input("메뉴를 선택하세요."))

                        if cmd == 1 :
                                show_list()
                        elif cmd == 2 :
                                search_id = input("검색할 회원의 아이디를 입력하세요 : ")
                                search(search_id)
                        elif cmd == 3 :
                                insert_user = input("등록할 회원 정보를 입력하세요.(id, name, pwd) : ")
                                insert_user = list(insert_user.split())
                                insert(insert_user)
                        elif cmd == 4 :
                                delete_user = input("삭제할 회원의 아이디를 입력하세요 : ")
                                delete(delete_user)
                        elif cmd == 5 :
                                break
                                cursor.close()
                                conn.close()
                        else :
                                raise ValueError
                except ValueError:
                        print("잘 못 입력했습니다. 다시 입력하세요.")

main()