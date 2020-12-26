from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QScrollBar, QHeaderView
from Layouts.main_ui import Ui_MainWindow
from Threads import threads as th
from Dialogs.details_dialog import DetailsDialog
import numpy as np
from datetime import datetime
import pandas as pd
import os


class MainForm(QMainWindow, Ui_MainWindow):
    len_row = 0
    customers = None
    categories = None
    sheet_customers = None
    first = True

    d_header = ['i', 'name', 'phone1', 'phone2', 'address', 'sales_p']

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('Assets\\icon.ico'))
        self.setWindowTitle('Customers - Main Window')

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.starting_thread()
        self.comName.currentTextChanged.connect(self.filter)
        self.comPhone.currentTextChanged.connect(self.filter)
        self.comAdmin_C.currentTextChanged.connect(self.filter)
        self.comAdmin_P.currentTextChanged.connect(self.filter)
        self.twResalt.itemDoubleClicked.connect(self.on_click_item)
        self.btnReset.clicked.connect(self.reset)
        self.actionNew_Customer.triggered.connect(self.new_customer)

        # Filter by company
        self.cbColth.stateChanged.connect(self.filter)
        self.cbOmega.stateChanged.connect(self.filter)
        self.cbYarn.stateChanged.connect(self.filter)

        # Filter by Customer type
        self.cbTager.stateChanged.connect(self.filter)
        self.cbTgerCloth.stateChanged.connect(self.filter)
        self.cbFactory.stateChanged.connect(self.filter)

        # filter by yarn categories
        self.cateYarnAll.stateChanged.connect(self.filter)
        self.cateSbun.stateChanged.connect(self.filter)
        self.cateCotton.stateChanged.connect(self.filter)
        self.cateFesskoz.stateChanged.connect(self.filter)
        self.cateLekra.stateChanged.connect(self.filter)
        self.cateShoayrat.stateChanged.connect(self.filter)
        self.cateMobant.stateChanged.connect(self.filter)
        self.catePolyster.stateChanged.connect(self.filter)
        self.cateMix.stateChanged.connect(self.filter)

        # filter by omega categories
        self.cateOmegaAll.stateChanged.connect(self.filter)
        self.cateHyaka.stateChanged.connect(self.filter)
        self.cateHarer.stateChanged.connect(self.filter)
        self.catePolysterTatrez.stateChanged.connect(self.filter)
        self.cateCerma.stateChanged.connect(self.filter)
        self.cateQassab.stateChanged.connect(self.filter)
        self.cateGoma.stateChanged.connect(self.filter)
        self.cateSpray.stateChanged.connect(self.filter)
        self.cateFazlin.stateChanged.connect(self.filter)

        # Display Categories
        self.btnYarn.clicked.connect(lambda: self.swCates.setCurrentIndex(0))
        self.btnOmega.clicked.connect(lambda: self.swCates.setCurrentIndex(1))
        self.btnCloth.clicked.connect(lambda: self.swCates.setCurrentIndex(2))

        # Disable While connecting
        self.comName.setEnabled(False)
        self.comPhone.setEnabled(False)
        self.groupBox_53.setEnabled(False)
        self.btnRefresh.setEnabled(False)

        self.btnRefresh.clicked.connect(self.fill_controls)

    def starting_thread(self):
        thread = th.GetAuth(self)
        thread.auth.connect(self.get_auth)
        thread.error.connect(self.thread_error)
        thread.off_data.connect(self.get_data)
        thread.start()

    def get_auth(self, sheet):
        if sheet is not None:
            thread = th.GetData(self)
            thread.sheet = sheet
            thread.data.connect(self.get_data)
            thread.error.connect(self.thread_error)
            thread.start()

    def thread_error(self, error):
        QMessageBox.warning(self, 'ERROR!', error)

    def get_data(self, customers, categories, sheet_customers, internet):
        self.customers = customers
        self.categories = categories
        self.sheet_customers = sheet_customers
        self.lblInternet.setText(internet)

        if not self.comName.isEnabled():
            self.fill_controls()
        else:
            self.filter()

        self.comName.setEnabled(1)
        self.comPhone.setEnabled(1)
        self.groupBox_53.setEnabled(1)
        self.btnRefresh.setEnabled(1)

        # self.fill_controls()

    def fill_controls(self):
        self.fill_table(data=self.customers[self.d_header].values.tolist())

    def fill_table(self, data=None):

        # Create table
        len_columns = len(self.d_header)
        if len(data) > 0:
            self.twResalt.setRowCount(len(data))

            self.twResalt.setColumnCount(len_columns)

            self.twResalt.setHorizontalHeaderLabels(
                ['Index', 'الاسم', 'رقم الموبيل', 'رقم الموبيل', 'المكان', 'مسؤول المبيعات'])
            if data is not None:
                for row in range(len(data)):
                    for column in range(len_columns):
                        self.twResalt.setItem(row, column, QTableWidgetItem(str(data[row][column])))
            if self.first:
                self.twResalt.resizeColumnsToContents()
                self.twResalt.resizeRowsToContents()
                self.first = 0
            self.twResalt.horizontalHeader()
        else:
            self.twResalt.setRowCount(len(data))

            self.twResalt.setColumnCount(len_columns)

    def on_click_item(self):
        index = self.twResalt.currentRow()
        code = int(self.twResalt.item(index, 0).text())
        self.details = DetailsDialog()
        self.details.customer = self.customers[self.customers['i'] == int(code)]
        self.details.sheet_row_index = self.customers[self.customers['i'] == int(code)].index[-1] + 2
        self.details.categories = self.categories
        self.details.sheet_customers = self.sheet_customers
        self.details.mode = 'v'
        self.details.setup_edit_view_mode(e_mode=False)
        self.details.set_data()
        self.details.show()

    def new_customer(self):
        self.details = DetailsDialog()
        self.details.categories = self.categories
        self.details.sheet_customers = self.sheet_customers
        self.details.mode = 'n'
        self.details.setup_edit_view_mode(e_mode=True)
        self.details.show()

    def filter(self):
        cb_companies = np.array([self.cbYarn.isChecked(), self.cbOmega.isChecked(), self.cbColth.isChecked()])
        cb_ctype = np.array([self.cbTager.isChecked(), self.cbFactory.isChecked(), self.cbTgerCloth.isChecked()])
        cb_cate_yarn = np.array([self.cateYarnAll.isChecked(), self.cateSbun.isChecked(), self.cateCotton.isChecked(),
                                 self.cateFesskoz.isChecked(), self.cateLekra.isChecked(),
                                 self.cateShoayrat.isChecked(), self.cateMobant.isChecked(),
                                 self.catePolyster.isChecked(), self.cateMix.isChecked()])

        cb_cate_omega = np.array([self.cateOmegaAll.isChecked(), self.cateHyaka.isChecked(), self.cateHarer.isChecked(),
                                  self.catePolysterTatrez.isChecked(), self.cateCerma.isChecked(),
                                  self.cateQassab.isChecked(), self.cateGoma.isChecked(),
                                  self.cateSpray.isChecked(), self.cateFazlin.isChecked()])

        _cate_yarn = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
        _cate_omega = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])

        _companies = ['yarn', 'omega', 'factory']

        # Companies Filter
        if all(cb_companies):
            result = self.customers[
                (self.customers['yarn'] == 1) & (self.customers['omega'] == 1) & (self.customers['factory'] == 1)]
            self.fill_table(data=result[self.d_header].values.tolist())
        elif not any(cb_companies):
            result = self.customers

            self.fill_table(data=result[self.d_header].values.tolist())

        elif sum(cb_companies) == 1:

            for i in range(len(cb_companies)):
                if cb_companies[i]:
                    result = self.customers[(self.customers[_companies[i]] == 1)]

            self.fill_table(data=result[self.d_header].values.tolist())

            '''
                if self.cbYarn.isChecked():
                    result = self.customers[(self.customers['yarn'] == 1)]
                elif self.cbOmega.isChecked():
                    result = self.customers[(self.customers['omega'] == 1)]
                else:
                    result = self.customers[(self.customers['factory'] == 1)]
            '''

        else:
            yarn = 1 if self.cbYarn.isChecked() else ''
            omega = 1 if self.cbOmega.isChecked() else ''
            cloth = 1 if self.cbColth.isChecked() else ''

            result = self.customers[
                (self.customers['yarn'] == yarn) &
                (self.customers['omega'] == omega) &
                (self.customers['factory'] == cloth)
                ]

            self.fill_table(data=result[self.d_header].values.tolist())

        # Customer type Filter
        if all(cb_ctype) or not any(cb_ctype):
            self.fill_table(data=result[self.d_header].values.tolist())

        else:
            ctype_ = np.array(['تاجر', 'مصنع', 'تاجر قماش'])

            result = result[(result['cust_type'].isin(ctype_[cb_ctype]))]

            self.fill_table(data=result[self.d_header].values.tolist())

        # Categories Filter
        '''
            customers[customers.yarn_cate.apply(lambda x: 'فسكوز' in x)]
            x in ['b', 'a', 'foo', 'bar'] for x in ['a', 'b']
        '''

        # filter by yarn categories
        if len(result) > 0:
            result = result[(result.yarn_cate.apply(
                lambda categories: all(
                    item in categories for item in self.categories['yarn'].loc[_cate_yarn[cb_cate_yarn]].values)) | (
                                 result.yarn_cate.apply(lambda x: 'الكل' in x)))]

            self.fill_table(data=result[self.d_header].values.tolist())

        # filter by omega categories
        if len(result) > 0:
            result = result[(result.omega_cate.apply(
                lambda categories: all(
                    item in categories for item in
                    self.categories['omega'].loc[_cate_omega[cb_cate_omega]].values))) | (
                                result.omega_cate.apply(lambda x: 'الكل' in x))]

            self.fill_table(data=result[self.d_header].values.tolist())

        # search by contact person
        if len(result) > 0:
            result = result[result.admin.str.contains(self.comAdmin_C.currentText())]
            self.fill_table(data=result[self.d_header].values.tolist())

        # Search by name
        if len(result) > 0:
            result = result[result.name.str.contains(self.comName.currentText())]
            self.fill_table(data=result[self.d_header].values.tolist())

        # Search by phone
        if len(result) > 0:
            phone = self.comPhone.currentText()
            result = result[
                result.phone1.str.contains(phone) | result.phone2.str.contains(phone) | result.phone3.str.contains(
                    phone) | result.phone4.str.contains(phone)]

            self.fill_table(data=result[self.d_header].values.tolist())

        # Search by sales person
        if len(result) > 0:
            result = result[result.sales_p.str.contains(self.comAdmin_P.currentText())]
            self.fill_table(data=result[self.d_header].values.tolist())

    def reset(self):
        self.comName.setCurrentText('')
        self.comPhone.setCurrentText('')
        self.comAdmin_C.setCurrentText('')
        self.comAdmin_P.setCurrentText('')

        # Filter by company
        self.cbColth.setChecked(False)
        self.cbOmega.setChecked(False)
        self.cbYarn.setChecked(False)

        # Filter by Customer type
        self.cbTager.setChecked(False)
        self.cbTgerCloth.setChecked(False)
        self.cbFactory.setChecked(False)

        # filter by yarn categories
        self.cateYarnAll.setChecked(False)
        self.cateSbun.setChecked(False)
        self.cateCotton.setChecked(False)
        self.cateFesskoz.setChecked(False)
        self.cateLekra.setChecked(False)
        self.cateShoayrat.setChecked(False)
        self.cateMobant.setChecked(False)
        self.catePolyster.setChecked(False)
        self.cateMix.setChecked(False)

        # filter by omega categories
        self.cateOmegaAll.setChecked(False)
        self.cateHyaka.setChecked(False)
        self.cateHarer.setChecked(False)
        self.catePolysterTatrez.setChecked(False)
        self.cateCerma.setChecked(False)
        self.cateQassab.setChecked(False)
        self.cateGoma.setChecked(False)
        self.cateSpray.setChecked(False)
        self.cateFazlin.setChecked(False)

        self.swCates.setCurrentIndex(0)
        vbar = self.scrollArea.verticalScrollBar()
        vbar.setValue(vbar.minimum())

        vbar = self.scrollArea_2.verticalScrollBar()
        vbar.setValue(vbar.minimum())

        vbar = self.scrollArea_3.verticalScrollBar()
        vbar.setValue(vbar.minimum())

        # self.scrollArea.setVerticalScrollBar(QScrollBar.to)
