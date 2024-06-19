import pandas as pd
import to_xl as xl
master_000 = {'cust_id':[1000001,1000000,1000000,1000000,1000001,1000001,1000001,1000001,1000001,1000001,1000001,1000001],
             'name':['B','A','A','A','B','B','B','B','B','B','B','B'],
             'gtin':['0100070919011022320200968613190124214002553673',
                     '0100070919011022320200945613190124214002553690',
                     '0100070919011022320200945613190124214002553690',
                     '0100070919011022320200945613190124214002553690',
                     '0100070919011022320200945613190124214002553690',
                     '0100070919011022320200945613190124214002553690',
                     '0100070919011022320200945613190124214002553690',
                     '019009642376897232010005791119010321327900304767',
                     '019009642376897232010005791119010321327900304767',
                     '019009642376897232010005791119010321327900304767',
                     '0100070919011022320200968613190124214002553673',
                     '0100070919011022320200968613190124214002553673',],
             'weight':[57.9,94.56,94.56,94.56,
                       94.56,94.56,94.56,
                       96.86,96.86,96.86,
                       57.9,57.9]
            }

master_001 = {'cust_id':[1000001,1000000,1000000,1000000,1000001,1000001,1000001,1000001,1000001,1000001,1000001,1000001],
             'name':['B','A','A','A','B','B','B','B','B','B','B','B'],
             'gtin':['00070919011022',
                     '00070919011022',
                     '90096423768972',
                     '90096423768972',
                     '90096423768972',
                     '00070919011022',
                     '00070919011022',
                     '90096423768972',
                     '90096423768972',
                     '90096423768972',
                     '90096423768972',
                     '00070919011022',],
             'weight':[57.9,94.56,94.56,
                       94.56,94.56,94.56,
                       94.56,96.86,96.86,
                       96.86,57.9,57.9]
            }
df = pd.DataFrame(master_001)
xl.excelify(df)