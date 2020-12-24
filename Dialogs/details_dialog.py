from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from Layouts.details_ui import Ui_details
from Threads.threads import PrintCustomer


class DetailsDialog(QDialog, Ui_details):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('Assets\\icon.ico'))
        self.btnEdit.clicked.connect(self.setup_edit_mode)
        self.mode = 'v'
        self.customer = None
        self.sheet_index = None

        self.fYarn.setVisible(False)
        self.fOmega.setVisible(False)
        self.fCloth.setVisible(False)

        if self.mode == 'v':
            self.setup_view_mode()
        elif self.mode == 'e':
            self.setup_edit_mode()

    def set_data(self):
        # print(self.customer['name'].values[-1])
        self.setWindowTitle(f"Details - {self.customer['name'].values[-1]}")

        self.lblName.setText(self.customer['name'].values[-1])
        self.txtSlaesP.setText(self.customer['sales_p'].values[-1])
        self.txtAdmin.setText(self.customer['admin'].values[-1])
        self.txtAdrress.setText(self.customer['address'].values[-1])
        self.txtMail.setText(self.customer['e_mail'].values[-1])
        self.txtPhone1.setText(
            f"0{self.customer['phone1'].values[-1]}" if self.customer['phone1'].values[-1] != '' else '')
        self.txtPhone2.setText(
            f"0{self.customer['phone2'].values[-1]}" if self.customer['phone2'].values[-1] != '' else '')
        self.txtPhone3.setText(
            f"0{self.customer['phone3'].values[-1]}" if self.customer['phone3'].values[-1] != '' else '')
        self.txtPhone4.setText(
            f"0{self.customer['phone4'].values[-1]}" if self.customer['phone4'].values[-1] != '' else '')

        self.txtCustType.setText(self.customer['cust_type'].values[-1])
        self.txtSize.setText(self.customer['size'].values[-1])

        self.cbYarn.setChecked(True if self.customer['yarn'].values[-1] == 1 else False)
        self.cbOmega.setChecked(True if self.customer['omega'].values[-1] == 1 else False)
        self.cbCloth.setChecked(True if self.customer['factory'].values[-1] == 1 else False)

        self.fill_table(data=self.customer['yarn_cate'].values[-1], obj=self.twYarn)
        self.fill_table(data=self.customer['omega_cate'].values[-1], obj=self.twOmega)
        self.fill_table(data=self.customer['factory_cate'].values[-1], obj=self.twCloth)

    def print_customer(self):
        thread = PrintCustomer(self)
        thread.customer = self.customer
        thread.prev_mode = False
        thread.error.connect(self.thread_error)
        thread.start()

    def prev_customer(self):
        thread = PrintCustomer(self)
        thread.customer = self.customer
        thread.error.connect(self.thread_error)
        thread.start()

    def setup_edit_mode(self):
        # self.lblName.setReadOnly(False)
        self.txtSlaesP.setReadOnly(False)
        self.txtAdmin.setReadOnly(False)
        self.txtAdrress.setReadOnly(False)
        self.txtMail.setReadOnly(False)
        self.txtPhone1.setReadOnly(False)
        self.txtPhone2.setReadOnly(False)
        self.txtPhone3.setReadOnly(False)
        self.txtPhone4.setReadOnly(False)
        self.txtCustType.setReadOnly(False)
        self.txtSize.setReadOnly(False)

        self.fYarn.setVisible(True)
        self.fOmega.setVisible(True)
        self.fCloth.setVisible(True)

        self.btnSave.setVisible(True)
        self.btnCancle.setVisible(True)

        self.btnPrint.setVisible(False)
        self.btnPrev.setVisible(False)

        self.cbYarn.setEnabled(True)
        self.cbOmega.setEnabled(True)
        self.cbCloth.setEnabled(True)

        self.btnCancle.clicked.connect(self.cancel_editing)

    def setup_view_mode(self):
        self.txtSlaesP.setReadOnly(True)
        self.txtAdmin.setReadOnly(True)
        self.txtAdrress.setReadOnly(True)
        self.txtMail.setReadOnly(True)
        self.txtPhone1.setReadOnly(True)
        self.txtPhone2.setReadOnly(True)
        self.txtPhone3.setReadOnly(True)
        self.txtPhone4.setReadOnly(True)
        self.txtCustType.setReadOnly(True)
        self.txtSize.setReadOnly(True)

        self.btnSave.setVisible(False)
        self.btnCancle.setVisible(False)

        self.btnPrint.setVisible(True)
        self.btnPrev.setVisible(True)

        self.fYarn.setVisible(False)
        self.fOmega.setVisible(False)
        self.fCloth.setVisible(False)

        self.cbYarn.setEnabled(False)
        self.cbOmega.setEnabled(False)
        self.cbCloth.setEnabled(False)

        self.btnPrint.clicked.connect(self.print_customer)
        self.btnPrev.clicked.connect(self.prev_customer)

    def cancel_editing(self):
        self.setup_view_mode()
        self.set_data()

    def thread_error(self, error):
        QMessageBox.warning(self, 'ERROR!', error)

    @staticmethod
    def fill_table(data=None, obj=None):
        # Create table
        len_columns = 1
        obj.setColumnCount(len_columns)
        if data is not None:
            obj.setRowCount(len(data))
        obj.setHorizontalHeaderLabels(['الاصناف'])
        obj.resizeColumnsToContents()
        obj.resizeRowsToContents()
        header = obj.horizontalHeader()
        header.setStretchLastSection(True)

        if data is not None:
            if len(data) > 0:
                for row in range(len(data)):
                    item = QTableWidgetItem(str(data[row]))
                    item.setTextAlignment(Qt.AlignHCenter)
                    obj.setItem(row, 0, item)
