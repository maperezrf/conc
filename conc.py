from operator import index
from wsgiref import validate
import pandas as pd 
from config import path
from dics import gcons, f12_vars, f3_vars, f11_vars, nc_vars, siebel_vars, ro_vars, mc_vars, en_vars, q_vars, siebel_vars
from os import listdir
from unidecode import unidecode

class CONC:

    dfs = []

    def  __init__(self) -> None:
        dcorte = '220816' #TODO input('Ingrese corte: ')
        self.path = path + '/'+ dcorte 
        files = listdir(self.path)
        self.file_name_list = ['f3', 'f11', 'f12', 'nc', 'ro', 'mc', 'en', 'quiebres', 'ss']
        self.file_name_dirs = get_dirs(files, self.file_name_list)

    def run(self):
        # Run 
        print('Cargando archivos ...')
        self.load_files()
        print('Transformando archivos ...')
        self.transform_files()
        print('Realizando uniones ...')
        self.res = self.get_join()
        print('Clasificando archivos ...')
        df = self.f12_classifier()
        print('Guardando archivos ...')
        df.to_csv('220817_resultado.csv', sep=';', index=False)
        df.to_csv('220817_resultado_v2.csv', index=False)
        print('Finalizado')


    def load_files(self):
        self.dfs = []
        for dir in self.file_name_dirs: 
            if dir != '':
                self.dfs.append(pd.read_csv(f'{self.path}/{dir}', sep=';', dtype='object'))
            else:
                self.dfs.append(pd.DataFrame())

    def transform_files(self):
        # PAP:  f3, f12, ro, en, siebel
        # MAP: f11, nc, mc, quiebres 
        col_key = [f3_vars['key'], f11_vars['key'], f12_vars['key'], nc_vars['key'], ro_vars['key'], mc_vars['key'], en_vars['key'], q_vars['key'], siebel_vars['key']]
        cols_dup = [f3_vars['dkeys'], f11_vars['dkeys'], f12_vars['dkeys'], nc_vars['dkeys'], ro_vars['dkeys'], mc_vars['dkeys'], en_vars['dkeys'], q_vars['dkeys'], siebel_vars['dkeys']]
        cols_num = [f3_vars['cnum'], f11_vars['cnum'], f12_vars['cnum'], nc_vars['cnum'], ro_vars['cnum'], mc_vars['cnum'], en_vars['cnum'], q_vars['cnum'], siebel_vars['cnum']]
        cols_string = [f3_vars['cstring'], f11_vars['cstring'], f12_vars['cstring'], nc_vars['cstring'], ro_vars['cstring'], mc_vars['cstring'], en_vars['cstring'], q_vars['cstring'], siebel_vars['cstring']]
        cols_to_keep = [f3_vars['ckeep'], f11_vars['ckeep'], f12_vars['ckeep'], nc_vars['ckeep'], ro_vars['ckeep'], mc_vars['ckeep'], en_vars['ckeep'], q_vars['ckeep'], siebel_vars['ckeep']]

        for i, df in enumerate(self.dfs):
            if df.empty == False: 
                self.dfs[i] = set_prefijo_df(self.dfs[i], self.file_name_list[i])
                self.dfs[i] = keep_cols(self.dfs[i], cols_to_keep[i])
                self.dfs[i] = clean_num(self.dfs[i], cols_num[i])
                self.dfs[i] = clean_string(self.dfs[i], cols_string[i])
                self.dfs[i] = delete_null_values(self.dfs[i], col_key[i])
                self.dfs[i] = delete_duplicates(self.dfs[i], cols_dup[i])             
            
    def get_dfs(self):
        return self.dfs 

    def f12_classifier(self):
        df = self.res.copy()

        val_entregas = df[f3_vars['key']].notna() | df[f11_vars['key']].notna() | df[mc_vars['key']].notna() | df[en_vars['key']].notna() | df[q_vars['key']].notna()
        df.loc[val_entregas, 'gco_ind_entregas'] = 'Tiene registro RO | MC | F3 | F11 | QUIEBRE'

        df.loc[df[siebel_vars['key']].notna() , 'gco_ind_ss_n3'] = 'Tiene SS' #TODO validar que ss sea nivel 3

        total_entrega = get_id_values(df, f12_vars['key'], f12_vars['estado'], ['TOTAL ENTREGA'])

        # ENTREGA ADMINISTRATIVA
        te_ent_admin = get_id_values(df, f12_vars['key'], f12_vars['subestado'], ['ENTREGA ADMINISTRATIVO'], total_entrega)
        mts_val = ['EN PROCESO NC', 'ENTREGADO EN TIENDA', 'FALTA STOCK', 'RETORNADO A ORIGEN', 'REFACTURACION', 'PROD CON NCRD']
        te_ea_mts = get_id_values(df, f12_vars['key'], f12_vars['mt'], mts_val, te_ent_admin)

        # ENTREGAS         
        entregas = ['ENTREGA POR PDA', 'ENTREGA EN SRX', 'ENTREGA PROVEEDOR']
        te_entregas = get_id_values(df, f12_vars['key'], f12_vars['subestado'], entregas, total_entrega)
        te_entregas_w_reg = get_id_values(df, f12_vars['key'], 'gco_ind_entregas', ['Tiene registro RO | MC | F3 | F11 | QUIEBRE'], te_entregas)
    
        # NO ENTREGAS 
        no_entregas = [ 'ENTREGA EN TIENDA','EN LINEA PRV. CON FACTURA', 'EN LINEA PRV. PEND. FACTURA', 'TOTAL ENTREGA']
        te_no_entregas = get_id_values(df, f12_vars['key'], f12_vars['subestado'], no_entregas, total_entrega)
        te_no_entregas_w_ss3 = get_id_values(df, f12_vars['key'], 'gco_ind_ss_n3', ['Tiene SS'], te_no_entregas)

        # RESULTADO 
        f12s_validos = te_ea_mts + te_entregas_w_reg + te_no_entregas_w_ss3
        return set_colvalue(df, f12_vars['key'], f12s_validos, 'gco_comment', 'Aplica conciliación')
    
    def get_join(self):

        # Uniones previas 
        self.dfs[1]['f11_folio_f12'] = self.dfs[1]['f11_observacion'].str.extract(r'^([1][2]\d{7,})') 
        self.dfs[1] = self.dfs[1].loc[~self.dfs[1]['f11_folio_f12'].isna()].reset_index(drop=True)
        self.dfs[1].drop_duplicates(['f11_folio_f12', 'f11_upc'], inplace=True)
        ne_ro = join( self.dfs[4], self.dfs[6],  'ro_ro', 'en_centrada', 'many_to_one') 

        # Inicio 
        f12_nc = join(self.dfs[2], self.dfs[3], ['f12_nfolio', 'f12_prd_upc'], ['nc_nfolio','nc_prod_ean_id'], 'one_to_one')
        f12_ss = join(f12_nc, self.dfs[8], 'f12_so', 'ss_suborden', 'many_to_one') # TODO No se encuentran coincidencias.
        f12_ro = join(f12_ss, ne_ro, ['f12_nfolio', 'f12_prd_upc'] , ['ro_do_inicial', 'ro_upc'], 'one_to_one')
        f12_mc = join(f12_ro, self.dfs[5], 'f12_nfolio' , 'mc_entrada', 'many_to_one')
        f12_f11 = join(f12_mc, self.dfs[1], ['f12_nfolio', 'f12_prd_upc'] , ['f11_folio_f12', 'f11_upc'], 'one_to_one')
        f12_f3 = join(f12_f11, self.dfs[0], ['f12_nfolio', 'f12_prd_upc'], ['f3_folio_f12', 'f3_upc'], 'one_to_one')
        f12_q = join(f12_f3, self.dfs[7], ['f12_nfolio', 'f12_prd_upc'], ['quiebres_f12', 'quiebres_codigo_barras'], 'one_to_one')
        return f12_q

def get_id_values(df, id_col, col, values, init_ids = []):
    todos = df[id_col].unique() if len(init_ids) == 0 else init_ids
    return list(df.loc[df[id_col].isin(todos) &  df[col].isin(values), id_col].unique())

def set_colvalue(df, id_col, ids,  comment_col, comment_value): 
    res = df.copy()
    res.loc[res[id_col].isin(ids), comment_col] = comment_value
    return res

def set_prefijo_df(df, prefijo): # TODO reescribir en list coprehension
    col = {}
    for i in df.columns:
        col[i] = f'{prefijo}_{i.lower()}'
    return df.rename(columns=col)

def delete_null_values(df, col): # PAP [x]
    return df.loc[~df[col].isna()].reset_index(drop=True)

def delete_duplicates(df, col_list): # MAP
    return df.drop_duplicates(col_list)

def clean_num(df, col_list): # PAP
    res = df.copy()
    for col in col_list:
        res.loc[:, col] = res[col].str.replace(r'([^0-9,])', '', regex=True)
        res.loc[:, col] = pd.to_numeric(res.loc[:, col] )
    return res

def clean_string(df, col_list): # MAP
    res = df.copy()
    for col in col_list:
        res[col] = res[col].fillna('nan')
        res[col] = res[col].apply(unidecode)
        res[col] = res[col].str.replace(r'([^a-zA-Z0-9-+(). ])', '', regex=True)
        res[col] = res[col].str.strip()
        res[col] = res[col].str.upper()
    return res

def keep_cols(df, cols_to_keep):
    return df.loc[:, cols_to_keep].reset_index(drop=True)

def get_dirs(files, file_name_list): # PAP [x]
    lista = []
    for name in file_name_list:
        flag = False 
        for file in files:
            if file.__contains__(name): 
                lista.append(file)
                flag = True
        if flag: 
            continue 
        else: 
            lista.append('')
    return lista 

def join(df_left, df_right, col_df_left, col_df_right, val_type):
    return df_left.merge(df_right, how = 'left', left_on = col_df_left, right_on = col_df_right, validate=val_type)

def innit_commandline():
    conc = CONC()
    conc.run()

if __name__=='__main__':
    innit_commandline()
