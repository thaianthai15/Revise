import datetime

# Tính tuổi
def calculate_age(year, current_year):
    age = current_year - year
    return age 

# Tìm tên năm sinh âm lịch
def calculate_lunar_year(year):
    lunar = ""
    match_can = {
        0: "Giáp",
        1: "Ất",
        2: "Bính",
        3: "Đinh",
        4: "Mậu",
        5: "Kỷ",
        6: "Canh",
        7: "Tân",
        8: "Nhâm",
        9: "Quý"
    }

    match_chi = {
        0: "Tý",
        1: "Sửu",
        2: "Dần",
        3: "Mão",
        4: "Thìn",
        5: "Tỵ",
        6: "Ngọ",
        7: "Mùi",
        8: "Thân",
        9: "Dậu",
        10: "Tuất",
        11: "Hợi",
    }

    # Tìm Căn
    can = match_can[(year - 3) % 10 - 1 ]
    # # Tìm Chi
    chi = match_chi[(year - 3) % 12 - 1]
    # Tên năm âm lịch gồm Căn và Chi
    lunar = can + " " + chi
    return lunar

# Tìm cung hoàng đạo 
def calculate_zodiac_signs(day, month):
    if not day or not month: 
        return "Không thể xem được cung nếu không biết ngày hoặc tháng sinh"
    else:
        if (day >= 21 and month == 3) or (day <= 19 and month == 4):
            return "Cung hoàng đạo của bạn là Bạch Dương - Aries"
        elif (day >= 21 and month == 4) or (day <= 20 and month ==5):
            return "Cung hoàng đạo của bạn là Kim Ngưu - Taurus"
        elif (day >= 21 and month == 5) or (day <= 21 and month == 6):
            return "Cung hoàng đạo của bạn là Song Tử - Gemini"
        elif (day >= 22 and month == 6) or (day <= 22 and month == 7):
            return "Cung hoàng đạo của bạn là Cự Giải - Cancer"
        elif (day >= 23 and month == 7) or (day <= 22 and month == 8):
            return "Cung hoàng đạo của bạn là Sư Tử  - Leo"
        elif (day >= 23 and month == 8) or (day <= 23 and month == 9):
            return "Cung hoàng đạo của bạn là Xử Nữ - Virgo"
        elif (day >= 23 and month == 9) or (day <= 23 and month == 10):
            return "Cung hoàng đạo của bạn là Thiên Bình - Libra"
        elif (day >= 23 and month == 10) or (day <= 23 and month == 11):
            return "Cung hoàng đạo của bạn là Bọ Cạp - Scorpio"
        elif (day >= 22 and month == 11) or (day <= 21 and month == 12):
            return "Cung hoàng đạo của bạn là Nhân Mã - Sagittarius"
        elif (day >= 22 and month == 12) or (day <= 19 and month == 1):
            return "Cung hoàng đạo của bạn là Ma Kết - Capricorn"
        elif (day >= 20 and month == 1) or (day <= 18 and month == 2):
            return "Cung hoàng đạo của bạn là Bảo Bình - Aquarius"
        else: 
            return "Cung hoàng đạo của bạn là Song Ngư - Pisces"


if __name__ == "__main__":
    x = datetime.datetime.now()
    current_year = x.year
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

    month = 0 
    while True:
        month_input = input("Hãy nhập tháng sinh của bạn (Có thể để trống): ")
        if month_input == "":
            break
        try:
            month = int(month_input)
            if 1 <= month <= 12:
                break
            else:
                print("Tháng sinh không hợp lệ")
        except:
            print("Tháng sinh sai định dạng")

    while True:
        try: 
            year = int(input("Hãy nhập năm sinh của bạn: "))
            if 1900 <= year <= current_year:
                break
            else: 
                print("Năm sinh không hợp lệ")
        except: 
            print("Năm sinh sai định dạng")

    print(f"Ngày tháng năm sinh của bạn là: {day}/{month}/{year}")
    print(f"Bạn năm nay {calculate_age(year, current_year)} tuổi")
    print(f"Tuổi âm của bạn là {calculate_lunar_year(year)}")
    print(calculate_zodiac_signs(day, month))