import datetime
import string
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="thai",
  passwd="123456",
  database="Age_Finder" # Dòng này sẽ chạy sau dòng tạo DB bên dưới, gỡ cmt dòng tạo db chạy trước rồi mới bỏ cmt dòng này
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE Age_Finder")
# mycursor.execute("CREATE TABLE users(userID INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), dob DATE, lunary_year VARCHAR(255), zodiac VARCHAR(255))")
# mycursor.execute("CREATE TABLE can (canID INT PRIMARY KEY, name VARCHAR(100))")
# mycursor.execute("CREATE TABLE chi (chiID INT PRIMARY KEY, name VARCHAR(100))")
# mycursor.execute("CREATE TABLE zodiac (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), start_day INT, start_month INT, end_day INT, end_month INT)")

# sql = "INSERT INTO can (canID, name) VALUES(%s, %s)"
# val = [
#     (1, 'Quý'),
#     (2, 'Giáp'),
#     (3, 'Ất'),
#     (4, 'Bính'),
#     (5, 'Đinh'),
#     (6, 'Mậu'),
#     (7, 'Kỷ'),
#     (8, 'Canh'),
#     (9, 'Tân'),
#     (10, 'Nhâm')
# ]
# sql2 = "INSERT INTO chi (chiID, name) VALUES(%s, %s)"
# val2 = [
#     (1, 'Hợi'),
#     (2, 'Tý'),
#     (3, 'Sửu'),
#     (4, 'Dần'),
#     (5, 'Mão'),
#     (6, 'Thìn'),
#     (7, 'Tỵ'),
#     (8, 'Ngọ'),
#     (9, 'Mùi'),
#     (10, 'Thân'),
#     (11, 'Dậu'),
#     (12, 'Tuất')
# ]

# sql3 = "INSERT INTO zodiac(name, start_day, start_month, end_day, end_month) VALUES(%s, %s, %s, %s ,%s)"
# val3 = [
#     ("Bảo Bình", 20, 1, 18, 2),
#     ("Song Ngư", 19, 2, 20, 3),
#     ("Bạch Dương", 21, 3, 19, 4),
#     ("Kim Ngưu", 20, 4, 20, 5),
#     ("Song Tử", 21, 5, 21, 6),
#     ("Cự Giải", 22, 6, 22, 7),
#     ("Sư Tử", 23, 7, 22, 8),
#     ("Xử Nữ", 23, 8, 22, 9),
#     ("Thiên Bình", 23, 9, 22, 10),
#     ("Bọ Cạp", 23, 10, 21, 11),
#     ("Nhân Mã", 22, 11, 21, 12),
#     ("Ma Kết", 22, 12, 19, 1)
# ]

# mycursor.executemany(sql, val)
# mycursor.executemany(sql2, val2)
# mycursor.executemany(sql3, val3)

# mydb.commit()

# Tính tuổi
def calculate_age(year, current_year):
    age = current_year - year
    return age 

# Tìm tên năm sinh âm lịch
def calculate_lunar_year(year):
    lunar = ""
    can = ""
    chi = ""
    # Tìm Căn ID
    can_id = (year - 3) % 10 + 1
    # Tìm Chi ID    
    chi_id = (year - 3) % 12 + 1

    sql = "SELECT * FROM can"
    mycursor.execute(sql)
    all_can = mycursor.fetchall()
    for row in all_can:
        if row[0] == can_id:
            can += row[1]
    
    sql2 = "SELECT * FROM chi"
    mycursor.execute(sql2)
    all_chi = mycursor.fetchall()
    for row in all_chi:
        if row[0] == chi_id:
            chi += row[1]

    # Tên năm âm lịch gồm Căn và Chi
    lunar = can + " " + chi
    return lunar  

def calculate_zodiac_signs(day, month):
    sql = "SELECT * FROM zodiac"
    mycursor.execute(sql)
    zodiac = mycursor.fetchall()
    for row in zodiac:
        # Row[3] là tháng bắt đầu, row[2] là ngày bắt đầu
        # Row[5] là tháng kết thúc, row[4] là ngày kết thúc
        start_date = (month == row[3] and day >= row[2])
        end_date = (month == row[5] and day <= row[4])
        if start_date or end_date:
            # Row[1] là tên cung
            return row[1]
        
# Hàm thêm các data người dùng input vào db 
def add_to_db(name, dob, lunar_year, zodiac=""):
    sql = "INSERT INTO users (name, dob, lunar_year, zodiac) VALUES (%s, %s, %s, %s)"
    data = (name, dob, lunar_year, zodiac)

    try:
        mycursor.execute(sql, data)
        mydb.commit()
        print(f"Thành công: {mycursor.rowcount} hàng được thêm vào.")
    except mysql.connector.Error as err:
        print(f"Lỗi: {err}")

# Hàm phân loại người dùng dựa vào cung và năm âm
def classify_user():
    sql = "SELECT * FROM users"
    mycursor.execute(sql)
    users = mycursor.fetchall()
    cung_dict = {}
    lunar_dict = {}

    for row in users:
        name = row[1]
        lunar_year = row[3]
        zodiac = row[4]

        if zodiac not in cung_dict:
            cung_dict[zodiac] = []
        cung_dict[zodiac].append(name)

        if lunar_year not in lunar_dict:
            lunar_dict[lunar_year] = []
        lunar_dict[lunar_year].append(name)
    return cung_dict, lunar_dict

# Hàm in ra danh sách các bạn ở trong các cung, các tuổi
def print_result(cung_dict, lunar_dict):
    print("---NHÓM CÁC BẠN THEO CUNG---")
    for cung, users in cung_dict.items():
        print(f"{cung}: {users}")

    print("---NHÓM CÁC BẠN SINH NĂM ÂM---")
    for lunar, users in lunar_dict.items():
        print(f"{lunar}: {users}")

if __name__ == "__main__":
    x = datetime.datetime.now()
    current_year = x.year
    # Validate ngày
    day = 0
    while True:
        day_input = input("Hãy nhập ngày sinh của bạn (Có thể để trống): ")
        if day_input == "":
            break
        try:
            day = int(day_input)
            if 1 <= day <= 31:
                break
            else:
                print("Ngày sinh không hợp lệ")
        except:
            print("Ngày sinh sai định dạng")
    # Validate tháng
    month = 0 
    while True:
        month_input = input("Hãy nhập tháng sinh của bạn (Có thể để trống): ")
        if month_input == "":
            if not day:
                break
        try:
            month = int(month_input)
            if 1 <= month <= 12:
                break
            else:
                print("Tháng sinh không hợp lệ")
        except:
            print("Tháng sinh không được chứa kí tự đặc biệt hoặc không được để trống nếu đã có ngày")
    # Validate năm
    while True:
        try: 
            year = int(input("Hãy nhập năm sinh của bạn: "))
            if 1900 <= year <= current_year:
                break
            else: 
                print("Năm sinh không hợp lệ")
        except: 
            print("Năm không được chứa kí tự đặc biệt hoặc để trống")
    # Validate tên
    while True:
        name = input("Nhập họ và tên của bạn: ").strip()
        
        if name.strip() == "":
            print("Tên không được để trống")
        elif not isinstance(name, str) or any(char in string.punctuation for char in name) or name.isdigit():
            print("Tên chỉ được chứa chữ cái")
        else:
            break

    lunar_year = calculate_lunar_year(year)
    zodiac = calculate_zodiac_signs(day, month)
    dob = f"{year}-{month}/{day}"

    print(f"Bạn năm nay: {calculate_age(year, current_year)} tuổi")
    print(f"Tuổi âm của bạn là: {lunar_year}")
    if zodiac == None:
        print("Không thể tính được cung hoàng đạo của bạn nếu không có ngày tháng sinh")
    else:
        print(f"Cung hoàng đạo của bạn là {zodiac}")

    add_to_db(name, dob, lunar_year, zodiac)
    cung_dict, lunar_dict = classify_user()
    print_result(cung_dict, lunar_dict)