from oauth2client.service_account import ServiceAccountCredentials
import gspread



# c = ''.join(['1', ',2', ',3'])
# print(type(c))

# define the scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('Assets\\token.json', scope)

# authorize the client sheet
client = gspread.authorize(creds)
sheet = client.open('customers')

sheet_customers = sheet.get_worksheet(0)

print(sheet_customers.cell(2, 1).value)
print(sheet_customers.acell('C7').value)


# def setup_view_mode(self):
#     self.lblName.setReadOnly(True)
#     self.txtSlaesP.setReadOnly(True)
#     self.txtAdmin.setReadOnly(True)
#     self.txtAdrress.setReadOnly(True)
#     self.txtMail.setReadOnly(True)
#     self.txtPhone1.setReadOnly(True)
#     self.txtPhone2.setReadOnly(True)
#     self.txtPhone3.setReadOnly(True)
#     self.txtPhone4.setReadOnly(True)
#     self.txtCustType.setReadOnly(True)
#     self.txtSize.setReadOnly(True)
#
#     self.btnSave.setVisible(False)
#     self.btnCancle.setVisible(False)
#
#     self.btnPrint.setVisible(True)
#     self.btnPrev.setVisible(True)
#
#     self.fYarn.setVisible(False)
#     self.fOmega.setVisible(False)
#     self.fCloth.setVisible(False)
#
#     self.cbYarn.setEnabled(False)
#     self.cbOmega.setEnabled(False)
#     self.cbCloth.setEnabled(False)
#
#     self.comSalesP.setVisible(False)
#     self.comCustType.setVisible(False)
#     self.comSize.setVisible(False)
#
#     self.txtSlaesP.setVisible(True)
#     self.txtCustType.setVisible(True)
#     self.txtSize.setVisible(True)
#
#     self.btnPrint.clicked.connect(self.print_customer)
#     self.btnPrev.clicked.connect(self.prev_customer)
