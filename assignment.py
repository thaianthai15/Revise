import datetime
import csv
import os
import string
# Tính tuổi
def calculate_age(year, current_year):
    age = current_year - year
    return age 

# Tìm tên năm sinh âm lịch
def calculate_lunar_year(year):
    lunar = ""
    match_can = {
        1: "Quý",
        2: "Giáp",
        3: "Ất",
        4: "Bính",
        5: "Đinh",
        6: "Mậu",
        7: "Kỷ",
        8: "Canh",
        9: "Tân",
        10: "Nhâm"
    }

    match_chi = {
        1: "Hợi",
        2: "Tý",
        3: "Sửu",
        4: "Dần",
        5: "Mão",
        6: "Thìn",
        7: "Tỵ",
        8: "Ngọ",
        9: "Mùi",
        10: "Thân",
        11: "Dậu",
        12: "Tuất",
    }

    # Tìm Căn
    can = match_can[(year - 3) % 10 + 1]
    # # Tìm Chi
    chi = match_chi[(year - 3) % 12 + 1]
    # Tên năm âm lịch gồm Căn và Chi
    lunar = can + " " + chi
    return lunar

# Tìm cung hoàng đạo -> Tạo 1 bảng để match -> 1 tên cung hoàng đạo, 1 ngày, 1 tháng 
# def calculate_zodiac_signs(day, month):
#     if not day or not month: 
#         return "Không thể xem được cung nếu không biết ngày hoặc tháng sinh"
#     else:
#         if (day >= 21 and month == 3) or (day <= 19 and month == 4):
#             return "Cung hoàng đạo của bạn là Bạch Dương - Aries"
#         elif (day >= 21 and month == 4) or (day <= 20 and month == 5):
#             return "Cung hoàng đạo của bạn là Kim Ngưu - Taurus"
#         elif (day >= 21 and month == 5) or (day <= 21 and month == 6):
#             return "Cung hoàng đạo của bạn là Song Tử - Gemini"
#         elif (day >= 22 and month == 6) or (day <= 22 and month == 7):
#             return "Cung hoàng đạo của bạn là Cự Giải - Cancer"
#         elif (day >= 23 and month == 7) or (day <= 22 and month == 8):
#             return "Cung hoàng đạo của bạn là Sư Tử  - Leo"
#         elif (day >= 23 and month == 8) or (day <= 23 and month == 9):
#             return "Cung hoàng đạo của bạn là Xử Nữ - Virgo"
#         elif (day >= 23 and month == 9) or (day <= 23 and month == 10):
#             return "Cung hoàng đạo của bạn là Thiên Bình - Libra"
#         elif (day >= 23 and month == 10) or (day <= 23 and month == 11):
#             return "Cung hoàng đạo của bạn là Bọ Cạp - Scorpio"
#         elif (day >= 22 and month == 11) or (day <= 21 and month == 12):
#             return "Cung hoàng đạo của bạn là Nhân Mã - Sagittarius"
#         elif (day >= 22 and month == 12) or (day <= 19 and month == 1):
#             return "Cung hoàng đạo của bạn là Ma Kết - Capricorn"
#         elif (day >= 20 and month == 1) or (day <= 18 and month == 2):
#             return "Cung hoàng đạo của bạn là Bảo Bình - Aquarius"
#         else: 
#             return "Cung hoàng đạo của bạn là Song Ngư - Pisces"


def calculate_zodiac_signs(day, month):
    # month bên trái, day bên phải
    signs = {
        (1, 20, 2, 18): "Bảo Bình - Aquarius",
        (2, 19, 3, 20): "Song Ngư - Pisces",
        (3, 21, 4, 19): "Bạch Dương - Aries",
        (4, 20, 5, 20): "Kim Ngưu - Taurus",
        (5, 21, 6, 21): "Song Tử - Gemini",
        (6, 22, 7, 22): "Cự Giải - Cancer",
        (7, 23, 8, 22): "Sư Tử  - Leo",
        (8, 23, 9, 22): "Xử Nữ - Virgo",
        (9, 23, 10, 22): "Thiên Bình - Libra",
        (10, 23, 11, 21): "Bọ Cạp - Scorpio",
        (11, 22, 12, 21): "Nhân Mã - Sagittarius",
        (12, 22, 1, 19): "Ma Kết - Capricorn"
    }

    for (m1, d1, m2, d2), name in signs.items():
        start_date = (month == m1 and day >= d1)
        end_date = (month == m2 and day <= d2)

        if start_date or end_date:
            return name

# Hàm thêm các data người dùng input vào file csv
def add_to_csv_file(name, dob, lunar_year, zodiac=""):
    mydict = [{'name': name, 'dob': dob, 'lunar_year': lunar_year, 'zodiac': zodiac}]
    filename = "data.csv"
    fields = ['name', 'dob', 'lunar_year', 'zodiac']

    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        if not file_exists:
            writer.writeheader()

        writer.writerows(mydict)

# Hàm phân loại người dùng dựa vào cung và năm âm
def classify_user(csvfile):
    cung_dict = {}
    lunar_dict = {}

    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        next(csv_reader)  

        for row in csv_reader:
            name = row[0]
            lunar_year = row[2]
            zodiac = row[3]

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
    dob = f"{day}/{month}/{year}"

    print(f"Bạn năm nay: {calculate_age(year, current_year)} tuổi")
    print(f"Tuổi âm của bạn là: {lunar_year}")
    if zodiac == None:
        print("Không thể tính được cung hoàng đạo của bạn nếu không có ngày tháng sinh")
    else:
        print(f"Cung hoàng đạo của bạn là {zodiac}")

    add_to_csv_file(name, dob, lunar_year, zodiac)
    cung_dict, lunar_dict = classify_user("data.csv")
    print_result(cung_dict, lunar_dict)