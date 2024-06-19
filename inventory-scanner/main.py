# Do I need some sort of #! thingy here?
import os
import pandas as pd
from _settings import CUSTOMERS, ACTIONS
import barcode_scanner as bs
import to_xl as xl
from pprint import pprint

master_dict = {'cust_id':[],
               'cust_name':[],
               'gtin':[],
               'gtin_name':[],
               'weight':[],}
customers = []
barcodes = []
datastream = []
error_barcodes = []
def pretty_customers(customer):
    for c in CUSTOMERS: 
        if str(c.uuid) == customer:
            return c.name
    return customer

'''
this function is a product of poor code design. 
1. You're mpn dict is calling excel and creating a new dict every time
2. You did this because you wanted to avoid creating a global variable 'MPN_DICT'
What's the solution here?
'''
def get_gtin_name(gtin):
    mpn_dict = get_mpn_dict()
    if gtin in mpn_dict:
        return mpn_dict[gtin]
    else:
        return 'No Name Found!'

def get_mpn_dict():
    curpath = os.path.dirname(__file__)
    # fn = os.path.abspath('C:\\Users\\Julie\\Documents\\dev\\inventory-scanner-git\\inventory-scanner\\docs\\master_mpn_list.xlsx')
    fn = os.path.abspath('C:\\Users\\User\\Dropbox\\master_mpn_list.xlsx')
    # C:\Users\User\Dropbox
    # fn = os.path.relpath('docs\\master_mpn_list.xlsx', curpath)
    df = pd.read_excel(fn, converters={'MPN': lambda x: str(x)}, index=False) #Keeps leading zeros for MPN
    mpn_dict = df.set_index('MPN').to_dict()['Description']
    return mpn_dict

def is_valid_gs1_128_barcode(input):
    # ensures >= 16 and starts with 01
    return (len(input) >= 16) and (input[0:2] == '01')

def is_valid_mexican_keken_barcode(input):
    # return (len(input) == 12 and input[:8] in keken_prod_ids)
    return input[6:8].lower() == 'd1'

def is_valid_australian_western_barcode(input):
    return input[-7:].lower() == '100018b' and len(input) == 29

#def is_valid_NewZealand_TeKuiti_lamb_barcode(input):
#    input[13:17]=='49400' and return len(input)==32    

def is_action(input):
    return input in ACTIONS.values()

def format_data(dictionary):
    df =  pd.DataFrame(dictionary)    
    df = df[['cust_id','cust_name','gtin','gtin_name','weight']]
    return df
def process_barcode(decoded):
    # Append formatted & decoded barcode to master_dict
    output = decoded
    master_dict['cust_id'].append(customers[-1:][0])
    master_dict['cust_name'].append(pretty_customers(customers[-1:][0]))
    master_dict['gtin'].append(output['GTIN-14'])
    master_dict['gtin_name'].append(get_gtin_name(output['GTIN-14']))
    master_dict['weight'].append(output['Product Net Weight'])

def main():
    #Initialize
    input_str = str(input('>> Customer: ')).lower()
    datastream.append(input_str)
    customers.append(input_str)
    # customers.append(Customer(input_str))

    while True:
        last_inp = datastream[-1:][0]
        print(last_inp)
        if last_inp.lower() == ACTIONS['exit']: 
            datastream.append('exit Logged')
            break
        elif last_inp.lower() == ACTIONS['next']:
            datastream.append('next Logged')
            new_customer = str(input('>> Please input your customer: '))
            customers.append(new_customer)
        else:
            last_customer = pretty_customers(customers[-1])
            # last_customer = customers[-1].name
            inp = str(input('>> Insert barcode for %s: '%last_customer))
            barcodes.append(inp)
            if is_valid_australian_western_barcode(inp):
                output = bs.australian_western_decoder(barcodes[-1])
                process_barcode(output)
            elif is_valid_gs1_128_barcode(inp):
                output = bs.gs1_decoder(barcodes[-1])
                process_barcode(output)
            elif is_valid_mexican_keken_barcode(inp):
                output = bs.mexican_keken_decoder(barcodes[-1])
                process_barcode(output)
            #elif is_valid_NewZealand_TeKuiti_lamb_barcode(inp):
            #    output = bs.NewZealand_TeKuiti_lamb_decoder(barcodes[-1])
            #    process_barcode(output)          
            elif is_action(inp):
                print('Action --%s-- occured'%inp)
            else:
                error_barcodes.append(inp)
                print('An error occurred! Barcode invalid. Add error handling!')
                continue
            datastream.append(inp)
    print("You have exited. Goodbye!")
    
    # Convert to Dataframe & Group It
    df = format_data(master_dict)
    ds = pd.DataFrame(datastream)
    eb = pd.DataFrame(error_barcodes)
    xl.excelify(df, ds, eb)
    
if __name__ == "__main__":
    main()
