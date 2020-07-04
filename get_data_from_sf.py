# -*- coding: utf-8 -*-
from pysuperfaktura.SFClient import SFClient
from pysuperfaktura.invoice import SFInvoiceClient, SFInvoice, SFInvoiceItem
from pysuperfaktura.expense import SFExpenseClient, SFExpense, SFExpenseItem
import datetime

api_client = SFClient('<email>', '<api_key>')

""" filtr: bezna, minuly mesic (hodnota 5) """
invfilter={'created': '5', 'type': 'regular', 'per_page': '1000'}
expfilter={'created': '5', 'per_page': '1000'}

invs=api_client.list_invoices(invfilter)
exps=api_client.list_expenses(expfilter)

total_amount=0
total_vat=0
kha5_amount=0
kha5_vat=0
kha4=[]
if (invs is not None):
    for inv in invs:
        item=inv.params.get("Invoice")
        item_name=item.get("name")
        item_invoiceno=item.get("invoice_no_formatted")
        item_amount=round(float(item.get("amount")), 2)
        item_vat=round(float(item.get("vat")), 2)
        item_dic=inv.params.get("Client").get("ic_dph")
        if (item_dic[:2]!="CZ"):
            print(u'Invalid DIC ({0})!'.format(item_dic))
        item_delivery=item.get("delivery").split()[0]
        dictitem={'name': item_name, 'amount': item_amount, 'vat': item_vat, 'DIC': item_dic, 'invoiceno': item_invoiceno, 'delivery_date': datetime.datetime.strptime(item_delivery, "%Y-%m-%d")}

        print(u'{0}: {1} / {2} | DIC={3}, no={4}, delivery={5}'.format(item_name, item_amount, item_vat, item_dic, item_invoiceno, item_delivery))
        total_amount+=item_amount
        total_vat+=item_vat
        if ((item_amount+item_vat)<=10000):
            kha5_amount+=item_amount
            kha5_vat+=item_vat
        else:
            kha4.append(dictitem)

    print('')

total_exp_amount=0
total_exp_vat=0
khb3_amount=0
khb3_vat=0
khb2=[]
if (exps is not None):
    for exp in exps:
        item=exp.params.get("Expense")
        item_name=item.get("name")
        item_invoiceno=item.get("document_number")
        item_amount=round(float(item.get("amount")), 2)
        item_vat=round((float(item.get("vat"))/100)*item_amount, 2)
        item_dic=exp.params.get("Client").get("ic_dph")
        if (item_dic[:2]!="CZ"):
            print(u'Invalid DIC ({0})!'.format(item_dic))
        item_delivery=item.get("delivery").split()[0]
        dictitem={'name': item_name, 'amount': item_amount, 'vat': item_vat, 'DIC': item_dic, 'invoiceno': item_invoiceno, 'delivery_date': datetime.datetime.strptime(item_delivery, "%Y-%m-%d")}

        print(u'{0}: -{1} / -{2} | DIC={3}, no={4}, delivery={5}'.format(item_name, item_amount, item_vat, item_dic, item_invoiceno, item_delivery))
        total_exp_amount+=item_amount
        total_exp_vat+=item_vat
        if ((item_amount+item_vat)<=10000):
            khb3_amount+=item_amount
            khb3_vat+=item_vat
        else:
            khb2.append(dictitem)

    print('')

dph=total_vat-total_exp_vat
dph_ctrl=(total_amount-total_exp_amount)*0.21
if (round(dph,1)!=round(dph_ctrl,1)):
    print('Pozor: nesedi kontrolni soucet DPH ({})!'.format(dph_ctrl))

print('Total Invoices: {0} / {1}'.format(total_amount, total_vat))
print('Total Expenses: {0} / {1}'.format(total_exp_amount, total_exp_vat))
print('DPH: {}\n'.format(dph))

""" Generovani XML - DPH """

minuly_mesic=datetime.date.today().month-1
minuly_rok=datetime.date.today().year
if minuly_mesic==0:
    minuly_mesic=12
    minuly_rok-=1

fn='DPHDP3-0000000000_{0}.xml'.format(datetime.date.today())
fxml=open(fn, 'w', newline='\n', encoding="utf-8")

""" Format viz https://adisepo.mfcr.cz/adistc/adis/idpr_pub/epo2_info/popis_struktury_detail.faces?zkratka=DPHDP3 """
fxml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><Pisemnost><DPHDP3>\n")
fxml.write("<VetaD d_poddp=\"{0}\" typ_platce=\"P\" c_okec=\"721000\" dokument=\"DP3\" k_uladis=\"DPH\" trans=\"A\" dapdph_forma=\"B\" rok=\"{1}\" mesic=\"{2}\" />\n".format(datetime.date.today().strftime("%d.%m.%Y"), minuly_rok, minuly_mesic))
fxml.write("<VetaP naz_obce=\"DOPLNIT\" c_pracufo=\"DOPLNIT\" jmeno=\"DOPLNIT\" c_telef=\"DOPLNIT\" prijmeni=\"DOPLNIT\" sest_prijmeni=\"DOPLNIT\" ulice=\"DOPLNIT\" sest_telef=\"DOPLNIT\" typ_ds=\"DOPLNIT\" dic=\"DOPLNIT\" sest_jmeno=\"DOPLNIT\" c_ufo=\"DOPLNIT\" psc=\"DOPLNIT\" stat=\"ČESKÁ REPUBLIKA\" c_pop=\"DOPLNIT\" email=\"DOPLNIT\" />\n")
fxml.write("<Veta1 dan23=\"{0}\" obrat23=\"{1}\" />\n".format(int(round(total_vat)), int(round(total_amount))))
fxml.write("<Veta4 odp_sum_nar=\"{0}\" odp_tuz23_nar=\"{0}\" pln23=\"{1}\" />\n".format(int(round(total_exp_vat)), int(round(total_exp_amount))))
fxml.write("<Veta6 dan_zocelk=\"{0}\" odp_zocelk=\"{1}\" dano_da=\"{2}\" />\n".format(int(round(total_vat)), int(round(total_exp_vat)), int(round(dph))))
fxml.write("</DPHDP3></Pisemnost>\n")

fxml.close()

""" Generovani XML - KH """
""" TODO: prazdne hlaseni """

fn='DPHKH1-0000000000_{0}.xml'.format(datetime.date.today())
fxml=open(fn, 'w', newline='\n', encoding="utf-8")

fxml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><Pisemnost><DPHKH1>\n")
fxml.write("<VetaD d_poddp=\"{0}\" dokument=\"KH1\" k_uladis=\"DPH\" khdph_forma=\"B\" rok=\"{1}\" mesic=\"{2}\" />\n".format(datetime.date.today().strftime("%d.%m.%Y"), minuly_rok, minuly_mesic))
fxml.write("<VetaP naz_obce=\"DOPLNIT\" c_pracufo=\"DOPLNIT\" jmeno=\"DOPLNIT\" c_telef=\"DOPLNIT\" prijmeni=\"DOPLNIT\" sest_prijmeni=\"DOPLNIT\" ulice=\"DOPLNIT\" sest_telef=\"DOPLNIT\" typ_ds=\"DOPLNIT\" dic=\"DOPLNIT\" sest_jmeno=\"DOPLNIT\" c_ufo=\"DOPLNIT\" psc=\"DOPLNIT\" stat=\"ČESKÁ REPUBLIKA\" c_pop=\"DOPLNIT\" email=\"DOPLNIT\" id_dats=\"DOPLNIT\" />\n")

""" uskutecnena plneni nad 10000Kc """
radek=1
for va4 in kha4:
    fxml.write("<VetaA4 dan1=\"{0}\" c_evid_dd=\"{1}\" kod_rezim_pl=\"0\" c_radku=\"{2}\" dppd=\"{3}\" dic_odb=\"{4}\" zdph_44=\"N\" zakl_dane1=\"{5}\" />\n".format(int(round(va4['vat'])), va4['invoiceno'], radek, va4['delivery_date'].strftime("%d.%m.%Y"), va4['DIC'][2:], int(round(va4['amount']))))
    radek+=1

""" uskutecnena plneni do 10000Kc """
if kha5_amount:
    fxml.write("<VetaA5 zakl_dane1=\"{0}\" dan1=\"{1}\" />\n".format(int(round(kha5_amount)), int(round(kha5_vat))))

""" narok na odpocet nad 10000Kc """
radek=1
for vb2 in khb2:
    fxml.write("<VetaB2 dan1=\"{0}\" c_evid_dd=\"{1}\" c_radku=\"{2}\" dppd=\"{3}\" dic_dod=\"{4}\" pomer=\"N\" zdph_44=\"N\" zakl_dane1=\"{5}\" />\n".format(int(round(vb2['vat'])), vb2['invoiceno'], radek, vb2['delivery_date'].strftime("%d.%m.%Y"), vb2['DIC'][2:], int(round(vb2['amount']))))
    radek+=1

""" narok na odpocet do 10000kc """
if khb3_amount:
    fxml.write("<VetaB3 zakl_dane1=\"{0}\" dan1=\"{1}\" />\n".format(int(round(khb3_amount)), int(round(khb3_vat))))

fxml.write("<VetaC pln23=\"{0}\" obrat23=\"{1}\" />\n".format(int(round(total_exp_amount)), int(round(total_amount))))
fxml.write("</DPHKH1></Pisemnost>\n")

fxml.close()
