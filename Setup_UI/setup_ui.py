from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from Layouts.main_ui import Ui_MainWindow
from Threads import threads as th
from Dialogs.details_dialog import DetailsDialog
import numpy as np
from Dialogs.loading_dialog import Loading
import json


class MainForm(QMainWindow, Ui_MainWindow):
    len_row = 0
    _data = None
    customers = None
    categories = None
    sales_p = None
    edit_requests = None
    auth_type = None
    sheet_customers = None
    sheet_requests = None
    first = True
    data_mode = 'c'

    d_header = ['i', 'name', 'phone1', 'phone2', 'address', 'sales_yarn', 'by']

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('Assets\\icon.ico'))
        self.setWindowTitle('Customers - Main Window')

        self.auth_account = json.load(open('Assets/token.json'))['client_email'].split('@')[0]
        print(self.auth_account)

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.loading = Loading()
        self.starting_thread()
        self.comName.currentTextChanged.connect(self._filter)
        self.comPhone.currentTextChanged.connect(self._filter)
        self.comContactPerson.currentTextChanged.connect(self._filter)
        self.comSalesPerson.currentTextChanged.connect(self._filter)
        self.twResalt.itemDoubleClicked.connect(self.on_click_item)
        self.btnReset.clicked.connect(self.reset)
        self.actionNew_Customer.triggered.connect(self.new_customer)

        # Filter by company
        self.cbColth.stateChanged.connect(self._filter)
        self.cbOmega.stateChanged.connect(self._filter)
        self.cbYarn.stateChanged.connect(self._filter)
        self.btnSearchData.clicked.connect(self.customer_data)
        self.btnRefresh.clicked.connect(self.requests_data)

        # Filter by Customer type
        self.cbTager.stateChanged.connect(self._filter)
        self.cbTgerCloth.stateChanged.connect(self._filter)
        self.cbFactory.stateChanged.connect(self._filter)

        # filter by yarn categories
        self.cateYarnAll.stateChanged.connect(self._filter)
        self.cateSbun.stateChanged.connect(self._filter)
        self.cateCotton.stateChanged.connect(self._filter)
        self.cateFesskoz.stateChanged.connect(self._filter)
        self.cateLekra.stateChanged.connect(self._filter)
        self.cateShoayrat.stateChanged.connect(self._filter)
        self.cateMobant.stateChanged.connect(self._filter)
        self.catePolyster.stateChanged.connect(self._filter)
        self.cateMix.stateChanged.connect(self._filter)

        # filter by omega categories
        self.cateOmegaAll.stateChanged.connect(self._filter)
        self.cateHyaka.stateChanged.connect(self._filter)
        self.cateHarer.stateChanged.connect(self._filter)
        self.catePolysterTatrez.stateChanged.connect(self._filter)
        self.cateCerma.stateChanged.connect(self._filter)
        self.cateQassab.stateChanged.connect(self._filter)
        self.cateGoma.stateChanged.connect(self._filter)
        self.cateSpray.stateChanged.connect(self._filter)
        self.cateFazlin.stateChanged.connect(self._filter)

        # Display Categories
        self.btnYarn.clicked.connect(lambda: self.swCates.setCurrentIndex(0))
        self.btnOmega.clicked.connect(lambda: self.swCates.setCurrentIndex(1))
        self.btnCloth.clicked.connect(lambda: self.swCates.setCurrentIndex(2))

        # Disable While connecting
        self.comName.setEnabled(False)
        self.comPhone.setEnabled(False)
        self.groupBox_53.setEnabled(False)
        self.btnRefresh.setEnabled(False)
        self.actionNew_Customer.setEnabled(False)
        self.btnSearchData.setVisible(False)

    def starting_thread(self):
        self.loading.start_dialog()
        thread = th.GetAuth(self)
        thread.auth.connect(self.get_auth)
        thread.error.connect(self.thread_error)
        thread.off_data.connect(self.get_data)
        thread.start()

    def get_auth(self, sheet):
        self.loading.start_dialog()
        if sheet is not None:
            thread = th.GetData(self)
            thread.sheet = sheet
            thread.data.connect(self.get_data)
            thread.error.connect(self.thread_error)
            thread.start()

    def thread_error(self, error):
        if not self.comName.isEnabled():
            self.loading.stop_dialog()
        QMessageBox.warning(self, 'ERROR!', error)

    def get_data(self, customers, categories, sales_p, edit_requests, auth, sheet_customers, sheet_requests, internet):
        try:
            self.auth_type = auth['permission'][auth['account'] == self.auth_account].values[-1]
        except:
            self.auth_type = 'editor'

        if self.auth_type == 'editor':
            edit_requests = edit_requests[edit_requests['by'] == self.auth_account]

        self._data = customers if self.data_mode == 'c' else edit_requests
        self.categories = categories
        self.sales_p = sales_p
        self.edit_requests = edit_requests
        self.customers = customers
        self.sheet_customers = sheet_customers
        self.sheet_requests = sheet_requests
        self.lblInternet.setText(internet)
        try:
            self.lcdNumber.setValue(len(edit_requests))
        except:
            self.lcdNumber.setValue(0)

        if not self.comName.isEnabled():
            self.fill_controls()
        else:
            self._filter()

        self.comName.setEnabled(1)
        self.comPhone.setEnabled(1)
        self.groupBox_53.setEnabled(1)
        self.btnRefresh.setEnabled(1)
        self.actionNew_Customer.setEnabled(1)
        self.loading.stop_dialog()

    def fill_controls(self):
        self.fill_table(data=self._data[self.d_header].values.tolist())

    def fill_table(self, data=None):

        # Create table
        len_columns = len(self.d_header)
        if len(data) > 0:
            self.twResalt.setRowCount(len(data))

            self.twResalt.setColumnCount(len_columns)

            self.twResalt.setHorizontalHeaderLabels(
                ['Index', 'الاسم', 'رقم الموبيل', 'رقم الموبيل', 'المكان', 'مسئول المبيعات', 'مسئول التعديل'])
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
        self.details.categories = self.categories
        self.details.sheet_customers = self.sheet_customers
        self.details.sheet_requests = self.sheet_requests
        self.details.sales_p = self.sales_p
        self.details.auth = self.auth_account
        self.details.auth_type = self.auth_type
        self.details.mode = 'v'

        if self.data_mode == 'c':
            self.details.customer = self._data[self._data['i'] == int(code)]
            self.details.sheet_row_index = self._data[self._data['i'] == int(code)].index[-1] + 2
            self.details.len_data = len(self._data)
            self.details.setup_edit_view_mode(e_mode=False)
        else:
            self.details.approve = True
            self.details.customer = self._data[self._data['i'] == int(code)]
            self.details.old_customer = self.customers[self.customers['i'] == int(code)]
            self.details.new_customer = self.details.customer
            self.details.sheet_row_index = self._data['row_index'].loc[self._data['i'] == int(code)].values[-1]
            self.details.setup_edit_view_mode(e_mode=True if self.auth_type == 'admin' else False)

        self.details.set_data()
        self.details.show()

    def new_customer(self):
        self.details = DetailsDialog()
        self.details.categories = self.categories
        self.details.sheet_customers = self.sheet_customers
        self.details.sheet_requests = self.sheet_requests
        self.details.sales_p = self.sales_p
        self.details.len_data = len(self._data)
        self.details.mode = 'n'
        self.details.auth = self.auth_account
        self.details.auth_type = self.auth_type
        self.details.sheet_row_index = self._data['i'].values[-1]
        self.details.setup_edit_view_mode(e_mode=True)
        self.details.show()

    def _filter(self):
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
            result = self._data[
                (self._data['yarn'] == 1) & (self._data['omega'] == 1) & (self._data['factory'] == 1)]
            self.fill_table(data=result[self.d_header].values.tolist())
        elif not any(cb_companies):
            result = self._data

            self.fill_table(data=result[self.d_header].values.tolist())

        elif sum(cb_companies) == 1:

            for i in range(len(cb_companies)):
                if cb_companies[i]:
                    result = self._data[(self._data[_companies[i]] == 1)]

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

            result = self._data[
                (self._data['yarn'] == yarn) &
                (self._data['omega'] == omega) &
                (self._data['factory'] == cloth)
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
            customers[customers.yarn_cate_name.apply(lambda x: 'فسكوز' in x)]
            x in ['b', 'a', 'foo', 'bar'] for x in ['a', 'b']
        '''

        # filter by yarn categories
        if len(result) > 0:
            result = result[(result.yarn_cate_name.apply(
                lambda categories: all(
                    item in categories for item in self.categories['yarn'].loc[_cate_yarn[cb_cate_yarn]].values)) | (
                                 result.yarn_cate_name.apply(lambda x: 'الكل' in x)))]

            self.fill_table(data=result[self.d_header].values.tolist())

        # filter by omega categories
        if len(result) > 0:
            result = result[(result.omega_cate_name.apply(
                lambda categories: all(
                    item in categories for item in
                    self.categories['omega'].loc[_cate_omega[cb_cate_omega]].values))) | (
                                result.omega_cate_name.apply(lambda x: 'الكل' in x))]

            self.fill_table(data=result[self.d_header].values.tolist())

        # search by contact person
        if len(result) > 0:
            result = result[result.contact_p.str.contains(self.comContactPerson.currentText())]
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
            result = result[result.sales_yarn.str.contains(self.comSalesPerson.currentText())]
            self.fill_table(data=result[self.d_header].values.tolist())

    def reset(self):
        self.comName.setCurrentText('')
        self.comPhone.setCurrentText('')
        self.comContactPerson.setCurrentText('')
        self.comSalesPerson.setCurrentText('')

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

    def customer_data(self):
        self.btnRefresh.setVisible(True)
        self.btnSearchData.setVisible(False)
        self._data = self.customers
        self.fill_controls()
        self.reset()
        self.data_mode = 'c'

    def requests_data(self):
        self.btnRefresh.setVisible(False)
        self.btnSearchData.setVisible(True)
        self._data = self.edit_requests
        self.fill_controls()
        self.reset()
        self.data_mode = 'e'
