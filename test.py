# from oauth2client.service_account import ServiceAccountCredentials
# import gspread
#
#
#
# # c = ''.join(['1', ',2', ',3'])
# # print(type(c))
#
# # define the scope
# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#
# # add credentials to the account
# creds = ServiceAccountCredentials.from_json_keyfile_name('Assets\\token.json', scope)
#
# # authorize the client sheet
# client = gspread.authorize(creds)
# sheet = client.open('customers')
#
# sheet_customers = sheet.get_worksheet(0)
#
# print(sheet_customers.cell(2, 1).value)
# print(sheet_customers.acell('C7').value)

#
# x = 'ممم'
# y = 'ممم '
#
# print(x == y)

# import json
#
# auth = json.load(open('Assets/Tokens/Omega.json'))['client_email'].split('@')[0]
#
# print(auth)

x = [1, 2, 3]
x[0] = 10
print(x)
