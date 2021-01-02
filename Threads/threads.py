import time
from shutil import copy2
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from openpyxl import load_workbook

temp_path = os.path.join(os.path.expanduser('~'), 'Documents\\Customers')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

online = 'متصل'
offline = 'غير متصل'
connecting = 'جاري محاولة الاتصال ...'
INTERNET = online

if not os.path.exists(temp_path):
    os.makedirs(temp_path)

if not os.path.exists(os.path.join(temp_path, 'temp.csv')):
    copy2(os.path.join(BASE_DIR, 'Assets\\temp.csv'), temp_path)
    # pd.DataFrame().to_csv(os.path.join(temp_path, 'temp.csv'), index=False, header=False,
    #                       encoding='utf-8-sig')

if not os.path.exists(os.path.join(temp_path, 'cate.csv')):
    copy2(os.path.join(BASE_DIR, 'Assets\\cate.csv'), temp_path)
    # pd.DataFrame().to_csv(os.path.join(temp_path, 'temp.csv'), index=False, header=False,
    #                       encoding='utf-8-sig')

if not os.path.exists(os.path.join(temp_path, 'sales_p.csv')):
    copy2(os.path.join(BASE_DIR, 'Assets\\sales_p.csv'), temp_path)
    # pd.DataFrame().to_csv(os.path.join(temp_path, 'sales_p.csv'), index=False, header=False,
    #                       encoding='utf-8-sig')

if not os.path.exists(os.path.join(temp_path, 'Customer Form.xlsx')):
    copy2(os.path.join(BASE_DIR, 'Assets\\Customer Form.xlsx'), temp_path)


def read_temp():
    customers = pd.read_csv(os.path.join(temp_path, 'temp.csv'), header=0, dtype={
        'phone1': 'str',
        'phone2': 'str',
        'phone3': 'str',
        'phone4': 'str'
    })
    customers = customers.replace(np.nan, '')

    customers['yarn_cate'] = customers['yarn_cate'].apply((lambda x: np.array(eval(x.replace(' ', ' ,')))))
    customers['omega_cate'] = customers['omega_cate'].apply((lambda x: np.array(eval(x.replace(' ', ' ,')))))
    customers['factory_cate'] = customers['factory_cate'].apply((lambda x: np.array(eval(x.replace(' ', ' ,')))))

    cate = pd.read_csv(os.path.join(temp_path, 'cate.csv'), header=0)
    cate = cate.set_index('code')
    cate = cate.replace(np.nan, '')

    sales_p = pd.read_csv(os.path.join(temp_path, 'sales_p.csv'), header=0)
    sales_p = sales_p.set_index('code')
    sales_p = sales_p.replace(np.nan, '')

    return customers, cate, sales_p


class GetAuth(QThread):
    auth = pyqtSignal(object)
    error = pyqtSignal(object)
    off_data = pyqtSignal(object, object, object, object, str)

    def run(self):
        no_internet = True
        first = 1
        while no_internet:
            try:
                # define the scope
                scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

                # add credentials to the account
                creds = ServiceAccountCredentials.from_json_keyfile_name('Assets\\token.json', scope)

                # authorize the client sheet
                client = gspread.authorize(creds)
                sheet = client.open('customers')

                self.auth.emit(sheet)
                no_internet = False
                INTERNET = online
            except Exception as e:
                no_internet = True
                INTERNET = offline
                if first:
                    self.error.emit(str(e))
                    first = 0

                cust, cate, sales_p = read_temp()
                self.off_data.emit(cust, cate, sales_p, None, INTERNET)

                time.sleep(5)
            print(INTERNET, datetime.time(datetime.now()))


class GetData(QThread):
    sheet = None
    data = pyqtSignal(object, object, object, object, str)
    error = pyqtSignal(object, object)

    def run(self):
        # get the first sheet of the Spreadsheet
        sheet_customers = self.sheet.get_worksheet(0)
        sheet_category = self.sheet.get_worksheet(1)
        sheet_sales_p = self.sheet.get_worksheet(2)

        while True:
            try:
                # convert the json to dataframe
                customers = pd.DataFrame.from_dict(sheet_customers.get_all_records())
                customers = customers.drop(index=0)
                customers = customers.replace(np.nan, '')
                customers = customers.astype({
                    'phone1': 'str',
                    'phone2': 'str',
                    'phone3': 'str',
                    'phone4': 'str'
                })

                # print(customers['phone1'])

                categories = pd.DataFrame.from_dict(sheet_category.get_all_records())
                categories = categories.set_index('code')

                sales_p = pd.DataFrame.from_dict(sheet_sales_p.get_all_records())
                sales_p = sales_p.set_index('code')

                customers['yarn_cate_name'] = customers['yarn_cate'].apply(lambda x: categories['yarn'].loc[
                    list(map(int, x.split(','))) if not isinstance(x, int) and x != '' else [] if x == '' else [
                        x]].values)

                customers['omega_cate_name'] = customers['omega_cate'].apply(lambda x: categories['omega'].loc[
                    list(map(int, x.split(','))) if not isinstance(x, int) and x != '' else [] if x == '' else [
                        x]].values)

                customers['factory_cate_name'] = customers['factory_cate'].apply(lambda x: categories['cloth'].loc[
                    list(map(int, x.split(','))) if not isinstance(x, int) and x != '' else [] if x == '' else [
                        x]].values)

                INTERNET = online
                self.data.emit(customers, categories, sales_p, sheet_customers, INTERNET)

                customers.to_csv(os.path.join(temp_path, 'temp.csv'), index=False, encoding='utf-8-sig')
                categories.to_csv(os.path.join(temp_path, 'cate.csv'), encoding='utf-8-sig')
                sales_p.to_csv(os.path.join(temp_path, 'sales_p.csv'), encoding='utf-8-sig')

            except:
                INTERNET = offline
                cust, cate, sales_p = read_temp()
                self.data.emit(cust, cate, sales_p, None, INTERNET)

            print(INTERNET, datetime.time(datetime.now()))
            time.sleep(10)


class PrintCustomer(QThread):
    customer = None
    prev_mode = True
    error = pyqtSignal(object)

    def run(self):
        try:
            form_path = os.path.join(temp_path, 'Customer Form.xlsx')

            wb = load_workbook(form_path)

            # grab the active worksheet
            ws = wb.active

            # Data can be assigned directly to cells
            ws['D1'] = self.customer['name'].values[-1]
            ws['E3'] = self.customer['sales_yarn'].values[-1]
            ws['E4'] = self.customer['contact_p'].values[-1]
            ws['E5'] = self.customer['address'].values[-1]
            ws['E6'] = f"0{self.customer['phone1'].values[-1]}" if self.customer['phone1'].values[-1] != '' else ''
            ws['H6'] = f"0{self.customer['phone2'].values[-1]}" if self.customer['phone2'].values[-1] != '' else ''
            ws['K6'] = f"0{self.customer['phone3'].values[-1]}" if self.customer['phone3'].values[-1] != '' else ''
            ws['E7'] = self.customer['e_mail'].values[-1]
            ws['E8'] = self.customer['cust_type'].values[-1]
            ws['E9'] = self.customer['size'].values[-1]
            ws['E10'] = str(self.customer['yarn_cate'].values[-1])
            ws['E11'] = str(self.customer['omega_cate'].values[-1])
            ws['E12'] = str(self.customer['factory_cate'].values[-1])

            # Save the file
            wb.save(form_path)
            if self.prev_mode:
                os.startfile(form_path)
            else:
                os.startfile(form_path, 'print')
        except Exception as e:
            self.error.emit(str(e))


class Save(QThread):
    sheet = None
    customer = None
    old_customer = None
    auth = None
    index = None
    mode = None
    len_data = None

    done = pyqtSignal()
    error = pyqtSignal(str)

    def run(self):
        try:
            row = [self.customer['i'], self.customer['sales_yarn'], self.customer['sales_omega'], self.customer['sales_cloth'],
                   self.customer['name'], self.customer['contact_p'], self.customer['branch'], self.customer['area'],
                   self.customer['address'], self.customer['phone1'], self.customer['phone2'], self.customer['phone3'],
                   self.customer['phone4'], self.customer['e_mail'], self.customer['omega_cate'],
                   self.customer['yarn_cate'], self.customer['factory_cate'], self.customer['size'],
                   self.customer['factory'], self.customer['yarn'], self.customer['omega'],
                   self.customer['cust_type'], self.customer['by']]

            if self.mode == 'n':
                self.sheet.insert_row(list(map(str, row)), self.len_data + 3)
            else:
                for col in range(len(row)):
                    self.sheet.update_cell(self.index, col + 1, str(row[col]))

            self.done.emit()
        except Exception as e:
            self.error.emit(str(e))
