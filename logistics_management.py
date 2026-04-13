import mysql.connector
import csv
from datetime import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="thai",
  passwd="123456",
  database="Logistics_Management" 
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE Logistics_Management")
# mycursor.execute("CREATE TABLE Area (AreaID INT AUTO_INCREMENT PRIMARY KEY, District VARCHAR(255))")
# mycursor.execute(
#     "CREATE TABLE Shipper (ShipperID INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Phone VARCHAR(255), AreaID INT, FOREIGN KEY (AreaID) REFERENCES Area(AreaID))"
# )
# mycursor.execute(
#     "CREATE TABLE Orders (OrderID INT AUTO_INCREMENT PRIMARY KEY, Price INT, ProductName VARCHAR(255), DeliveryAddress VARCHAR(255), CustomerName VARCHAR(255), CustomerPhone VARCHAR(255), CreatedAt DATE, Status VARCHAR(255), ShipperID INT, FOREIGN KEY (ShipperID) REFERENCES Shipper(ShipperID))"
# )
# mycursor.execute(
#     "CREATE TABLE Order_History ("
#     "ID INT AUTO_INCREMENT PRIMARY KEY, "
#     "OrderID INT, "
#     "ShipperID INT, "
#     "Status VARCHAR(50), "
#     "CreatedAt DATE, "
#     "FOREIGN KEY (OrderID) REFERENCES Orders(OrderID), "
#     "FOREIGN KEY (ShipperID) REFERENCES Shipper(ShipperID))"
# )

areas = [
        "Ba Đình", "Hoàn Kiếm", "Cầu Giấy", "Hai Bà Trưng", "Hoàng Mai", "Đống Đa",
        "Tây Hồ", "Thanh Xuân", "Bắc Từ Liêm", "Hà Đông", "Long Biên", "Nam Từ Liêm",
        "Ba Vì", "Chương Mỹ", "Đan Phượng", "Đông Anh", "Gia Lâm", "Hoài Đức", "Mê Linh",
        "Mỹ Đức", "Phú Xuyên", "Phúc Thọ", "Quốc Oai", "Sóc Sơn", "Thạch Thất",
        "Thanh Oai", "Thanh Trì", "Thường Tín", "Ứng Hòa", "Sơn Tây"
]

# Tạo khu vực vận chuyển
def create_area():
    while True:
        district = input("Mời nhập khu vực vận chuyển (quận/huyện): ").strip()

        if district == "":
            print("Tên quận/huyện không được để trống")
            continue

        if district not in areas:
            print("Tên quận/huyện không hợp lệ")
            continue

        break 

    sql = "INSERT INTO Area (district) VALUES (%s)"
    mycursor.execute(sql, (district,))
    mydb.commit()

    print("Thêm khu vực mới thành công")

# Tạo thông tin shipper
def create_shipper():
    while True:
        while True:
            name = input("Mời nhập tên shipper: ")
            if name.strip() == "" or name.isdigit():
                print("Tên không được để trống hoặc chứa số")
            else:
                break

        while True:
            phone = input("Mời nhập số điện thoại: ")
            if phone.strip() == "" or not phone.isdigit() or len(phone) != 10:
                print("Số điện thoại phải gồm 10 chữ số")
            else:
                break

        while True:
            district = input("Mời nhập khu vực vận chuyển (quận/huyện): ").strip()

            if district == "":
                print("Tên quận/huyện không được để trống")
                continue

            if district not in areas:
                print("Tên quận/huyện không hợp lệ")
                continue
            break 

        break

    sql = "SELECT AreaID FROM Area WHERE district = %s"
    mycursor.execute(sql, (district, ))
    result = mycursor.fetchone()

    if not result:
        print("Khu vực này chưa khả dụng")
        return
    
    area_id = result[0]

    sql2 = "INSERT INTO Shipper(Name, Phone, AreaID) VALUES (%s, %s, %s)"
    data = (name, phone, area_id)

    mycursor.execute(sql2, data)
    mydb.commit()

    print("Thêm shipper mới thành công")


# Tạo đơn hàng
def create_order():
    while True:
        product_name = input("Mời nhập tên sản phẩm: ")
        if product_name.strip() == "":
            print("Tên sản phẩm không được để trống")
            continue
            
        customer_name = input("Mời nhập tên người nhận: ")
        if customer_name.strip() == "":
            print("Tên người nhận không được để trống")
            continue
    
        phone = input("Mời nhập số điện thoại người nhận: ")
        if phone.strip() == "" or not phone.isdigit() or len(phone) != 10:
            print("Số điện thoại phải gồm 11 chữ số")
            continue

        price = input("Mời nhập giá sản phẩm: ")
        if not price.isdigit() or int(price) <= 0:
            print("Giá phải là số dương")
            continue
        price = int(price)

        address = input("Hãy nhập địa chỉ người nhận: ")
        if address.strip() == "":
            print("Địa chỉ không được để trống")
            continue

        break

    now = datetime.now()
    mycursor.execute("SELECT ShipperID FROM Shipper ORDER BY RAND() LIMIT 1")
    shipper = mycursor.fetchone() 

    if not shipper:
        print("Không có shipper khả dụng hiện tại")
        return 
    
    shipper_id = shipper[0]

    sql = "INSERT INTO Orders (ProductName, CustomerName, CustomerPhone, DeliveryAddress, Price, Status, CreatedAt, ShipperID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    data = (product_name, customer_name, phone, address, price, "Pending", now, shipper_id)

    mycursor.execute(sql, data)
    mydb.commit()

    order_id = mycursor.lastrowid

    sql2 = "INSERT INTO Order_History(OrderID, ShipperID, Status, CreatedAt) VALUES (%s, %s, %s, %s)"
    data2 = (order_id, shipper_id, "Pending", now)
    mycursor.execute(sql2, data2)
    mydb.commit()

    print("Tạo đơn hàng thành công!")

# Cập nhật đơn hàng
def update_order():
    while True:
        order_id = input("Nhập mã đơn: ")
        if not order_id.isdigit():
            print("Mã đơn không hợp lệ")
            continue
        else:
            order_id = int(order_id)
            break

    sql = "SELECT * FROM Orders WHERE OrderID = %s"
    mycursor.execute(sql, (order_id, ))
    if not mycursor.fetchone():
        print("Đơn không tồn tại")
        return

    print("1. Đổi trạng thái")
    print("2. Đổi shipper")
    choice = input("Mời nhập lựa chọn: ")

    now = datetime.now()

    if choice == "1":
        while True: 
            status = input("Trạng thái mới (Pending/Delivering/Delivered/Failed): ")

            valid_status = ["Pending", "Delivering", "Delivered", "Failed"]

            if status not in valid_status:
                print("Trạng thái không hợp lệ")
                continue
            break 

        sql2 = "UPDATE Orders SET Status= %s WHERE OrderID= %s"
        data = (status, order_id)
        mycursor.execute(sql2, data)

        sql3 = "SELECT ShipperID FROM Orders WHERE OrderID= %s"
        mycursor.execute(sql3, (order_id, ))
        shipper_id = mycursor.fetchone()[0]

        sql4 = "INSERT INTO Order_History(OrderID, ShipperID, Status, CreatedAt) VALUES (%s,%s,%s,%s)"
        data2 = (order_id, shipper_id, status, now)
        mycursor.execute(sql4, data2)

    elif choice == "2":
        while True:
            new_shipper = input("Nhập shipper mới: ")
            if not new_shipper.isdigit() or int(new_shipper) <= 0:
                print("Shipper ID không hợp lệ")
                continue
            else:
                new_shipper = int(new_shipper)
                break

        sql5 = "SELECT * FROM Shipper WHERE ShipperID = %s"
        mycursor.execute(sql5, (new_shipper, ))
        if not mycursor.fetchone():
            print("Shipper không tồn tại")
            return

        sql6 = "UPDATE Orders SET ShipperID= %s WHERE OrderID= %s"
        data3 = (new_shipper, order_id)
        mycursor.execute(sql6, data3)

        sql7 = "INSERT INTO Order_History(OrderID, ShipperID, Status, CreatedAt) VALUES (%s,%s,%s,%s)"
        data4 = (order_id, new_shipper, "Transferred", now)
        mycursor.execute(sql7, data4)

    mydb.commit()
    print("Cập nhật thành công")

# Thống kê nhân sự theo vùng
def list_shipper():
    while True:
        district = input("Mời nhập vùng cần thống kê: ")
        if district.strip() == "" or district.isdigit():
            print("Hãy nhập đúng tên quận/huyện")
        else:
            break 

    sql = "SELECT Name, Phone FROM Shipper WHERE AreaID = (SELECT AreaID FROM Area WHERE District = %s)"

    mycursor.execute(sql, (district, ))
    result = mycursor.fetchall()

    if not result:
        print("Không có shipper trong khu vực này hoặc khu vực không tồn tại")
        return
    
    filename = "report.csv"
    fields = ['Name', 'Phone']

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        data = []
        for row in result:
            data.append({
                'Name': row[0],
                'Phone': row[1],
            })

        writer.writerows(data)

    print("Xuất file báo cáo thành công!")

# Báo cáo công việc/hiệu suất
def report_work():
    while True:
        shipper_id = input("Mời nhập mã nhân viên bạn muốn thống kê: ")
        if not shipper_id.isdigit() or int(shipper_id) <= 0:
            print("Mã nhân viên không hợp lệ")
        else:
            shipper_id = int(shipper_id)
            break

    sql = "SELECT Price FROM Orders WHERE ShipperID = %s AND Status = 'Delivered'"
    mycursor.execute(sql, (shipper_id, ))
    result = mycursor.fetchall()

    if not result:
        print("Shipper này chưa có đơn hàng nào")
        return

    total_value = 0
    for row in result:
        total_value += row[0]
    print(f"Tổng doanh thu: {total_value}")

def find_order():
    while True:
        order_id = input("Nhập mã đơn: ")
        if not order_id.isdigit():
            print("Mã đơn không hợp lệ")
            continue
        else:
            break

    sql = "SELECT CreatedAt, (SELECT Name FROM Shipper s WHERE s.ShipperID = h.ShipperID) AS Name, Status FROM Order_History h WHERE OrderID = %s ORDER BY CreatedAt"
    mycursor.execute(sql, (order_id, ))
    result = mycursor.fetchall()

    if not result:
        print("Không tìm thấy")
        return

    print("LỊCH SỬ ĐƠN HÀNG:")
    for row in result:
        print(f"{row[0]} - {row[1]} - {row[2]}")


if __name__ == "__main__":
    while True:
        print("---Chào mừng tới hệ thống Logistics---")
        print("1. Tạo khu vực")
        print("2. Tạo shipper")
        print("3. Tạo đơn")
        print("4. Cập nhật đơn")
        print("5. Thống kê shipper")
        print("6. Tra cứu đơn")
        print("7. Báo cáo công việc")
        print("0. Thoát chương trình")

        choice = input("Mời bạn nhập lựa chọn: ")

        if choice == "1":
            create_area()
        elif choice == "2":
            create_shipper()
        elif choice == "3":
            create_order()
        elif choice == "4":
            update_order()
        elif choice == "5":
            list_shipper()
        elif choice == "6":
            find_order()
        elif choice == "7":
            report_work()
        elif choice == "0":
            break
    
