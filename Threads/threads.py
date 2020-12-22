import time
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import numpy as np
import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

temp_path = os.path.join(os.path.expanduser('~'), 'Documents\\Customers')

online = 'متصل'
offline = 'غير متصل'
connecting = 'جاري محاولة الاتصال ...'
INTERNET = online

if not os.path.exists(temp_path):
    os.makedirs(temp_path)
    pd.DataFrame().to_csv(os.path.join(temp_path, 'temp.csv'), index=False, header=False,
                          encoding='utf-8-sig')
elif not os.path.exists(os.path.join(temp_path, 'temp.csv')):
    pd.DataFrame().to_csv(os.path.join(temp_path, 'temp.csv'), index=False, header=False,
                          encoding='utf-8-sig')

elif not os.path.exists(os.path.join(temp_path, 'cate.csv')):
    pd.DataFrame().to_csv(os.path.join(temp_path, 'temp.csv'), index=False, header=False,
                          encoding='utf-8-sig')


def read_temp():
    customers = pd.read_csv(os.path.join(temp_path, 'temp.csv'), header=0, dtype={
        'phone1': 'str',
        'phone2': 'str',
        'phone3': 'str',
        'phone4': 'str'
    })
    customers = customers.replace(np.nan, '')

    customers['yarn_cate'] = customers['yarn_cate'].apply((lambda x: np.array(eval(x.replace(' ', ' ,')))))
    #
    customers['omega_cate'] = customers['omega_cate'].apply((lambda x: np.array(eval(x.replace(' ', ' ,')))))
    customers['factory_cate'] = customers['factory_cate'].apply((lambda x: np.array(eval(x.replace(' ', ' ,')))))

    cate = pd.read_csv(os.path.join(temp_path, 'cate.csv'), header=0)
    cate = cate.set_index('code')
    cate = cate.replace(np.nan, '')

    return customers, cate


class GetAuth(QThread):
    auth = pyqtSignal(object)
    error = pyqtSignal(object)
    off_data = pyqtSignal(object, object, str)

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

                cust, cate = read_temp()
                self.off_data.emit(cust, cate, INTERNET)

                time.sleep(5)
            print(INTERNET, datetime.time(datetime.now()))


class GetData(QThread):
    sheet = None
    data = pyqtSignal(object, object, str)
    error = pyqtSignal(object, object)

    def run(self):
        # get the first sheet of the Spreadsheet
        sheet_customers = self.sheet.get_worksheet(0)
        sheet_category = self.sheet.get_worksheet(1)

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
                    'phone4': 'str',
                    'yarn_cate': 'str'
                })

                # print(customers['phone1'])

                categories = pd.DataFrame.from_dict(sheet_category.get_all_records())

                categories = categories.set_index('code')
                customers['yarn_cate'] = customers['yarn_cate'].apply(lambda x: categories['yarn'].loc[
                    list(map(int, x.split(','))) if not isinstance(x, int) and x != '' else [] if x == '' else [
                        x]].values)

                customers['omega_cate'] = customers['omega_cate'].apply(lambda x: categories['omega'].loc[
                    list(map(int, x.split(','))) if not isinstance(x, int) and x != '' else [] if x == '' else [
                        x]].values)

                customers['factory_cate'] = customers['factory_cate'].apply(lambda x: categories['cloth'].loc[
                    list(map(int, x.split(','))) if not isinstance(x, int) and x != '' else [] if x == '' else [
                        x]].values)

                INTERNET = online
                self.data.emit(customers, categories, INTERNET)

                customers.to_csv(os.path.join(temp_path, 'temp.csv'), index=False, encoding='utf-8-sig')
                categories.to_csv(os.path.join(temp_path, 'cate.csv'), encoding='utf-8-sig')
            except:
                INTERNET = offline
                cust, cate = read_temp()

                self.data.emit(cust, cate, INTERNET)
            print(INTERNET, datetime.time(datetime.now()))
            time.sleep(3)
