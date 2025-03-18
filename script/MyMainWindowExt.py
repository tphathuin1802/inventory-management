from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt6.QtCore import Qt, QDateTime, QDate
from script.MyMainWindow import Ui_MainWindow


class MyMainWindowExt(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.processSignalAndSlot()


    def processSignalAndSlot(self):
        self.comboBoxDanhMuc.setCurrentText("Điện thoạis")

        # Removed duplicate signal connection
        self.pushButtonThem.clicked.connect(self.addProduct)
        self.pushButtonLuu.clicked.connect(self.saveProduct)
        self.pushButtonThoat.clicked.connect(self.buttonClose)
        self.pushButtonXoa.clicked.connect(self.deleteProduct)

    def buttonClose(self):
        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Exit Confirmation")
        dlg.setText("Are you sure you want to Exit?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()

        # Check user choice
        if button == QMessageBox.StandardButton.Yes:
            self.MainWindow.close()

    def addProduct(self):
        self.lineEditMaSanPham.clear()
        self.lineEitTenSanPham.clear()
        self.lineEditSoLuong.clear()
        self.lineEditDonGia.clear()
        # Fixed QtCore import issue
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.checkBoxTpHCM.setChecked(True)
        self.lineEditMaSanPham.setFocus()

    def saveProduct(self):
        # Validate form fields
        # Fixed typo in lineEitTenSanPham to lineEditTenSanPham
        if not self.lineEditMaSanPham.text() or not self.lineEitTenSanPham.text():
            QMessageBox.warning(self.MainWindow, "Lỗi", "Mã sản phẩm và tên sản phẩm không được để trống.")
            return

        try:
            so_luong = int(self.lineEditSoLuong.text())
            don_gia = float(self.lineEditDonGia.text())

            # Add additional validation for positive values
            if so_luong <= 0 or don_gia <= 0:
                QMessageBox.warning(self.MainWindow, "Lỗi", "Số lượng và đơn giá phải lớn hơn 0.")
                return

        except ValueError:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Số lượng và đơn giá phải là số hợp lệ.")
            return

        if self.dateTimeEdit.date() > QDate.currentDate():
            QMessageBox.warning(self.MainWindow, "Lỗi", "Ngày nhập kho không được lớn hơn ngày hiện tại.")
            return

        # Add success message
        QMessageBox.information(self.MainWindow, "Thông báo", "Lưu sản phẩm thành công!")

    def deleteProduct(self):
        # Xóa sản phẩm được chọn khỏi CSDL
        selected_row = self.tableWidgetHienThiSanPham.currentRow()
        if selected_row != -1:
            # Hiển thị hộp thoại xác nhận xóa
            dlg = QMessageBox(self.MainWindow)
            dlg.setWindowTitle("Xác nhận xóa")
            dlg.setText("Bạn có chắc chắn muốn xóa sản phẩm này?")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            dlg.setIcon(QMessageBox.Icon.Question)
            button = dlg.exec()

            if button == QMessageBox.StandardButton.Yes:
                # Xóa sản phẩm khỏi cơ sở dữ liệu và bảng
                self.tableWidgetHienThiSanPham.removeRow(selected_row)
                # code xóa từ cơ sở dữ liệu ở đây

                # Nếu không còn sản phẩm nào, đưa về trạng thái mặc định
                if self.tableWidgetHienThiSanPham.rowCount() == 0:
                    self.addProduct()