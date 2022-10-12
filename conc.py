from operator import index
from wsgiref import validate
import pandas as pd 
from config import path
from dics import gcons, f12_vars, f3_vars, f11_vars, nc_vars, siebel_vars, ro_vars, mc_vars, en_vars, q_vars, siebel_vars, tesor_nc, tesor_sieb, pos_loc, columns_res_sac_nnt_nss
from os import listdir
from unidecode import unidecode
from datetime import datetime
import numpy as np 
pd.options.display.max_columns = 500

class CONC:

    dfs = []
    dt = datetime.now().strftime('%y%m%d')

    def  __init__(self) -> None:
        dcorte = input('Ingrese corte: ')
        self.path_input = path + '/input' + '/'+ dcorte 
        self.path_output = path + '/output'
        files = listdir(self.path_input)
        self.file_name_list = ['f3', 'f11', 'f12', 'nc', 'ro', 'mc', 'en', 'quiebres', 'ss', 'tesoreria_ntc', 'tesoreria_sieb']
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
        self.set_up_exit(df)
        res = input('¿Distribuir bases? (y/n)')
        if res == 'y':
            self.save_results(df)
        print('Finalizado')


    def load_files(self):
        self.dfs = []
        for dir in self.file_name_dirs: 
            if dir != '':
                self.dfs.append(pd.read_csv(f'{self.path_input}/{dir}', sep=';', dtype='object'))
            else:
                self.dfs.append(pd.DataFrame())

    def transform_files(self):
        col_key = [f3_vars['key'], f11_vars['key'], f12_vars['key'], nc_vars['key'], ro_vars['key'], mc_vars['key'], en_vars['key'], q_vars['key'], siebel_vars['key'], tesor_nc['key'], tesor_sieb['key']]
        cols_dup = [f3_vars['dkeys'], f11_vars['dkeys'], f12_vars['dkeys'], nc_vars['dkeys'], ro_vars['dkeys'], mc_vars['dkeys'], en_vars['dkeys'], q_vars['dkeys'], siebel_vars['dkeys'], tesor_nc['dkeys'], tesor_sieb['dkeys']]
        cols_num = [f3_vars['cnum'], f11_vars['cnum'], f12_vars['cnum'], nc_vars['cnum'], ro_vars['cnum'], mc_vars['cnum'], en_vars['cnum'], q_vars['cnum'], siebel_vars['cnum'], tesor_nc['cnum'], tesor_sieb['cnum']]
        cols_string = [f3_vars['cstring'], f11_vars['cstring'], f12_vars['cstring'], nc_vars['cstring'], ro_vars['cstring'], mc_vars['cstring'], en_vars['cstring'], q_vars['cstring'], siebel_vars['cstring'], tesor_nc['cstring'], tesor_sieb['cstring']]
        cols_to_keep = [f3_vars['ckeep'], f11_vars['ckeep'], f12_vars['ckeep'], nc_vars['ckeep'], ro_vars['ckeep'], mc_vars['ckeep'], en_vars['ckeep'], q_vars['ckeep'], siebel_vars['ckeep'], tesor_nc['ckeep'], tesor_sieb['ckeep']]

        for i, df in enumerate(self.dfs):
            if df.empty == False: 
                self.dfs[i] = set_prefijo_df(self.dfs[i], self.file_name_list[i])
                self.dfs[i] = keep_cols(self.dfs[i], cols_to_keep[i])
                self.dfs[i] = clean_num(self.dfs[i], cols_num[i])
                self.dfs[i] = clean_string(self.dfs[i], cols_string[i])
                self.dfs[i] = delete_null_values(self.dfs[i], col_key[i])
                self.dfs[i] = delete_duplicates(self.dfs[i], cols_dup[i])             
        
        # Transformaciones adicionales 
        self.dfs[2].loc[:, f12_vars['fpactada']] = pd.to_datetime(self.dfs[2][f12_vars['fpactada']], format='%Y-%m-%d')
        cond_fpactada = (self.dfs[2][f12_vars['fpactada']]< datetime.now() )& (self.dfs[2][f12_vars['fpactada']].notna())
        self.dfs[2].loc[cond_fpactada, f12_vars['ind_fpactada']] = 'OVERDUE'
        self.dfs[2].loc[~cond_fpactada, f12_vars['ind_fpactada']] = 'ON TIME'
        self.dfs[2].loc[self.dfs[2][f12_vars['nc']] == '0', f12_vars['nc']] = np.nan

    def get_dfs(self):
        return self.dfs 

    def f12_classifier(self):
        df = self.res.copy()

        for i in pos_loc:
            df.loc[(df['f12_gco_inc_nc'] == 'Tiene NC') & (df['f12_loc_nc'] == i) & (~df['f12_nterminal'].isin(pos_loc[i])), 'gco_ind_pos' ] = 'POS de tienda'  
            df.loc[(df['f12_gco_inc_nc'] == 'Tiene NC') & (df['f12_loc_nc'] == i) & (df['f12_nterminal'].isin(pos_loc[i])), 'gco_ind_pos' ] = 'POS de SAC'  
        

        val_entregas = (df[f3_vars['key']].notna()) | (df[f11_vars['key']].notna()) | (df[mc_vars['key']].notna()) | (df[en_vars['key']].notna()) | (df[q_vars['key']].notna())|(df[ro_vars['key']].notna())
        df.loc[val_entregas, 'gco_ind_entregas'] = 'Tiene registro RO | MC | F3 | F11 | QUIEBRE'

        df.loc[df[siebel_vars['key']].notna() , 'gco_ind_ss'] = 'Tiene SS'
        df.loc[df[siebel_vars['n3']].str.contains(r'TROCADO|AVERIA|INCOMPLETO|ENTREGA FALSO|ENTREGA FALSA', na = False), 'gco_ind_ss_n3'] = 'Se encontró TROCADO|AVERIA|INCOMPLETO|ENTREGA FALSA en SS N3'

        # Se encontro en base tesoreria
        df.loc[(df[tesor_nc['cod_aut']].notna()) | ((df[tesor_sieb['sieb_ss']].notna()) ), 'gco_ind_btes'] = 'La NC|SS existe en DB tesorería' 
        df.loc[df['gco_ind_btes'].isna(), 'gco_ind_btes' ] = 'La NC|SS no existe en DB tesorería'

        # Unificacion estados, base tesoreria
        df.loc[df[tesor_nc['estado']].isna(), tesor_nc['estado']] = df.loc[df[tesor_nc['estado']].isna(), tesor_sieb['estado_sieb']].values
        df.rename(columns = {tesor_nc['estado']: 'estado_tesoreria'}, inplace=True)

        # Se realizo el pago
        df.loc[((df[tesor_nc['cod_aut']].notna()) | ((df[tesor_sieb['sieb_ss']].notna()))) & (df['estado_tesoreria'] == 'PROCESADA'), 'gco_ind_registra_pago'] = 'Pago procesado'
        df.loc[((df[tesor_nc['cod_aut']].notna()) | ((df[tesor_sieb['sieb_ss']].notna()))) & (df['gco_ind_registra_pago'].isna()), 'gco_ind_registra_pago' ] = 'Pago rechazado'

        total_entrega = get_id_values(df, f12_vars['key'], f12_vars['estado'], ['TOTAL ENTREGA'])

        # C1 ENTREGA ADMINISTRATIVA
        te_ent_admin = get_id_values(df, f12_vars['key'], f12_vars['subestado'], ['ENTREGA ADMINISTRATIVO'], total_entrega)
        mts_val = ['EN PROCESO NC', 'ENTREGADO EN TIENDA', 'FALTA STOCK', 'RETORNADO A ORIGEN', 'REFACTURACION', 'PROD CON NCRD']
        c1 = get_id_values(df, f12_vars['key'], f12_vars['mt'], mts_val, te_ent_admin)

        # C2 ENTREGAS         
        entregas = ['ENTREGA POR PDA', 'ENTREGA EN SRX', 'ENTREGA PROVEEDOR']
        te_entregas = get_id_values(df, f12_vars['key'], f12_vars['subestado'], entregas, total_entrega)
        c2 = get_id_values(df, f12_vars['key'], 'gco_ind_entregas', ['Tiene registro RO | MC | F3 | F11 | QUIEBRE'], te_entregas)
    
        # C3 NO ENTREGAS 
        no_entregas = [ 'ENTREGA EN TIENDA','EN LINEA PRV. CON FACTURA', 'EN LINEA PRV. PEND. FACTURA', 'TOTAL ENTREGA']
        te_no_entregas = get_id_values(df, f12_vars['key'], f12_vars['subestado'], no_entregas, total_entrega)
        c3 =  get_id_values(df, f12_vars['key'], 'gco_ind_ss_n3', ['Se encontró TROCADO|AVERIA|INCOMPLETO|ENTREGA FALSA en SS N3'], te_no_entregas)

        # C4 ANULADO POR NCRD
        ancdr_est = get_id_values(df, f12_vars['key'], f12_vars['estado'], ['ANULADO X NCRD'] )
        c4 = get_id_values(df, f12_vars['key'], f12_vars['subestado'], ['ANULADO X NCRD'], ancdr_est)

        # C5 EN RUTA Y DIGITADO 
        ## EN RUTA
        en_ruta = get_id_values(df, f12_vars['key'], f12_vars['estado'], ['EN RUTA'] )
        er_se_values =['EN RUTA AL CLIENTE', 'MT PROVEEDOR', 'EN TRANSITO', 'MT']
        er_se = get_id_values(df, f12_vars['key'], f12_vars['subestado'], er_se_values , en_ruta)
        c5_p1 = get_id_values(df, f12_vars['key'], f12_vars['ind_fpactada'], ['OVERDUE'], er_se)

        ## DIGITADO
        digitados = get_id_values(df, f12_vars['key'], f12_vars['estado'], ['DIGITADO'] )
        dig_se_values =['BOLETEADO/FACTURADO', 'MT PROVEEDOR']
        dig_se = get_id_values(df, f12_vars['key'], f12_vars['subestado'], dig_se_values, digitados)
        c5_p2 =get_id_values(df, f12_vars['key'], f12_vars['ind_fpactada'], ['OVERDUE'], dig_se)

        # RESULTADO 
        f12s_validos = c1 + c2 + c3 + c4 + c5_p1 + c5_p2
        return set_colvalue(df, f12_vars['key'], f12s_validos, 'gco_comment', 'Aplica conciliación')
    
    def get_join(self):
        
        # Uniones previas 
        self.dfs[1][f11_vars['f11_f12']] = self.dfs[1][f11_vars['observ_f11']].str.extract(r'(?!S{2} [1]-[1][2])(^[1][2]\d{7,})') 
        self.dfs[1].loc[self.dfs[1][f11_vars['f11_f12']].isna(), f11_vars['f11_f12']] = self.dfs[1].loc[self.dfs[1][f11_vars['f11_f12']].isna(), f11_vars['observ_f11']].str.extract(r'(?!S{2} [1]-[1][2])( [1][2]\d{7,})').values
        self.dfs[1][f11_vars['f11_f12']] = self.dfs[1][f11_vars['f11_f12']].str.strip()
        self.dfs[1] = self.dfs[1].loc[~self.dfs[1][f11_vars['f11_f12']].isna()].reset_index(drop=True)
        self.dfs[1].drop_duplicates([f11_vars['f11_f12'], f11_vars['upc_f11']], inplace=True)
        ne_ro = join( self.dfs[4], self.dfs[6],  ro_vars['ro'], en_vars['centrada'], 'many_to_one') 
        print('union 1 ')

        # Uniendo base de SS por sub orden y nro f12
        f12_ss_1 = join(self.dfs[2], self.dfs[8].loc[(self.dfs[8]['ss_suborden'].notna()) & (self.dfs[8]['ss_suborden'] != 0)], f12_vars['so'], siebel_vars['sorden'], 'many_to_many')
        ss_x_f12 = self.dfs[8].drop_duplicates([siebel_vars['f12']]) 
        f12_ss = f12_ss_1.merge(self.dfs[8].loc[(self.dfs[8]['ss_num_f12'].notna()) & (self.dfs[8]['ss_num_f12'] != 0)], how = 'left', left_on = f12_vars['folio'],right_on = siebel_vars['f12'], suffixes=('', '_y')) 
        f12_ss.loc[(f12_ss[siebel_vars['ss_y']].notna()), siebel_vars['ckeep'] ] = f12_ss.loc[(f12_ss[siebel_vars['ss_y']].notna()), gcons['union_ss_aux']].values
        f12_ss.drop(columns = gcons['union_ss_aux'], inplace = True) # Se eliminan columnas de segunda Base
        f12_ss.drop_duplicates(['f12_nfolio','f12_prd_upc'], inplace=True) #TODO revisar cual ss es la verdadera del f12
        print('union 2 ')

        # Uniendo base tesoreria_nc por cautoriza y ss 
        f12_tes_ntc_1 = join(f12_ss, self.dfs[9], f12_vars['nc'], tesor_nc['cod_aut'], 'many_to_one')
        tes_ntc_x_ss = self.dfs[9].drop_duplicates([tesor_nc['ntc_ss']]) 
        f12_tes_ntc = f12_tes_ntc_1.merge(tes_ntc_x_ss, how = 'left', left_on = siebel_vars['f12'], right_on = tesor_nc['ntc_ss'], suffixes=('', '_y')) 
        f12_tes_ntc.loc[(f12_tes_ntc[tesor_nc['ntc_ss_y']].notna()), tesor_nc['ckeep']] = f12_tes_ntc.loc[(f12_tes_ntc[tesor_nc['ntc_ss_y']].notna()), gcons['union_tes_ntc_aux']].values
        f12_tes_ntc.drop(columns = gcons['union_tes_ntc_aux'], inplace = True) # Se eliminan columnas de segunda Base
        print('union 3 ')
        # #Continuan unioines
        
        f12_tes_ss = join(f12_tes_ntc, self.dfs[10], siebel_vars['ss'], tesor_sieb['sieb_ss'], 'many_to_one')
        f12_ro = join(f12_tes_ss, ne_ro, [f12_vars['folio'], f12_vars['upc']] , [ro_vars['do_inicial'], ro_vars['upc_ro']], 'one_to_one')
        f12_mc = join(f12_ro, self.dfs[5], f12_vars['folio'] , mc_vars['entrada_mc'], 'many_to_one')
        f12_f11 = join(f12_mc, self.dfs[1], [f12_vars['folio'], f12_vars['upc']] , [f11_vars['f11_f12'], f11_vars['upc_f11']], 'one_to_one')
        f12_f3 = join(f12_f11, self.dfs[0], [f12_vars['folio'], f12_vars['upc']], [f3_vars['f3_f12'], f3_vars['upc_f3']], 'one_to_one')
        f12_q = join(f12_f3, self.dfs[7], [f12_vars['folio'], f12_vars['upc']], [q_vars['f12_q'], q_vars['q_ean']], 'one_to_one')
        return f12_q

    def set_up_exit(self, df):
        res_ant = pd.read_csv('C:/Users/maperezr/OneDrive - Falabella/General/DATA/CONC/pbi/resultado_agg.csv', sep=';', dtype='object')
        df = df.loc[(df['f12_nfolio'].isin(res_ant['f12_nfolio'].unique())) & (df['f12_dcreacion']<'2022-07-31')]
        locales = pd.read_csv('C:/Users/maperezr/OneDrive - Falabella/General/DATA/listado_locales.csv', dtype = 'object', usecols = ['LOC_ID','LOCAL_AGG'])
        df = df.merge(locales, how='left', left_on = 'f12_loc_id', right_on = 'LOC_ID')
        df.loc[df['gco_ind_ss'].isna(), 'gco_ind_ss'] = 'No tiene SS'
        df.loc[df['gco_comment'].isna(), 'gco_comment'] = 'No aplíca conciliación'
        gco_cols = ['gco_ind_entregas', 'gco_ind_ss', 'gco_ind_ss_n3', 'gco_comment', 'gco_ind_btes', 'estado_tesoreria', 'gco_ind_registra_pago', 'LOCAL_AGG']
        return df 
        # df[f12_vars['ckeep']+gco_cols].to_csv(f'{self.path_output}/{self.dt}_resultado.csv', sep=';', index=False)

    def save_results(self, df):
        df['f12_nfolio'] = pd.to_numeric(df['f12_nfolio'])
        res_sac = pd.read_excel('C:/Users/maperezr/Downloads/pablo.xlsx', dtype='object', usecols = ['f12_nfolio', 'comentarios_resp_rev'])
        res_sac.rename(columns={'comentarios_resp_rev':'comentarios_resp_rev_ant'}, inplace=True)
        res_sac['f12_nfolio'] = pd.to_numeric(res_sac['f12_nfolio'])
        nac_snc_sss =  df.loc[(df['f12_gco_inc_nc'] == 'Tiene NC') & (df['gco_comment'] == 'No aplíca conciliación') & (df['f12_desc_estado'] == 'TOTAL ENTREGA') & (df['gco_ind_ss'] == 'Tiene SS')].reset_index(drop = True)
        nac_snc_sss = nac_snc_sss.merge(res_sac, how='left', on='f12_nfolio')
        print('No aplica conciliacion, Tiene NC, Tiene SS')
        print(f'F12\'s {nac_snc_sss.f12_nfolio.nunique()}')
        print(f'SKU {nac_snc_sss.shape[0]}')
        nac_snc_sss.to_excel(f'output/{self.dt}_e1_nac_snc_sss.xlsx', index= False)

        sac_nnc = df.loc[(df['f12_gco_inc_nc'] == 'No tiene NC') & (df['gco_comment'] == 'Aplica conciliación')].reset_index(drop =True)
        print('Aplica conciliacion, No tiene NC')
        print(f'F12\'s {sac_nnc.f12_nfolio.nunique()}')
        print(f'SKU {sac_nnc.shape[0]}')

        sac_nnc_sss = sac_nnc.loc[(sac_nnc['gco_ind_ss'] == 'Tiene SS') & (sac_nnc['ss_fcr'] == 'N')].reset_index(drop =True)
        print('Aplica conciliacion, No tiene NC, Tiene SS')
        print(f'F12\'s {sac_nnc_sss.f12_nfolio.nunique()}')
        print(f'SKU {sac_nnc_sss.shape[0]}')
        sac_nnc_sss.to_excel(f'output/{self.dt}_e2_sac_nnc_sss.xlsx', index= False)

        print('Aplica conciliacion,  No tiene NC, No tiene SS')
        sac_nnc_nss = sac_nnc.loc[(sac_nnc['gco_ind_ss'] == 'No tiene SS')].reset_index(drop =True)
        usr = pd.read_excel('input/220509_usr_locales (2).xlsx', usecols=['Usuario','Local agg'])
        usr.rename(columns={'Local agg':'Local usr cierre'}, inplace = True)
        sac_nnc = sac_nnc.reindex(columns_res_sac_nnt_nss)
        sac_nnc_nss = sac_nnc_nss.merge(usr, how = 'left', left_on='f12_username', right_on = 'Usuario')
        print(f'F12\'s {sac_nnc_nss.f12_nfolio.nunique()}')
        print(f'SKU {sac_nnc_nss.shape[0]}')

        sac_nnc_nss_cd =  sac_nnc_nss.loc[sac_nnc_nss['Local usr cierre'] == 'CD'].reset_index(drop =True)
        print('Aplica conciliacion, Tiene NC, No tiene NC, CD')
        print(f'F12\'s {sac_nnc_nss_cd.f12_nfolio.nunique()}')
        print(f'SKU {sac_nnc_nss_cd.shape[0]}')
        sac_nnc_nss_cd.to_excel(f'output/{self.dt}_e3_sac_nnc_nss_cd.xlsx', index= False)

        sac_nnc_nss_tiendas =  sac_nnc_nss.loc[sac_nnc_nss['Local usr cierre'] == 'TIENDA'].reset_index(drop =True)
        print('Aplica conciliacion, Tiene NC, No tiene NC, Tienda')
        print(f'F12\'s {sac_nnc_nss_tiendas.f12_nfolio.nunique()}')
        print(f'SKU {sac_nnc_nss_tiendas.shape[0]}')
        sac_nnc_nss_tiendas.to_excel(f'output/{self.dt}_e4_sac_nnc_nss_tiendas.xlsx', index= False)

        sac_nnc_nss_sistemas =  sac_nnc_nss.loc[sac_nnc_nss['Local usr cierre'] == 'SISTEMAS'].reset_index(drop =True)
        print('Aplica conciliacion, Tiene NC, No tiene NC, Sistemas')
        print(f'F12\'s {sac_nnc_nss_sistemas.f12_nfolio.nunique()}')
        print(f'SKU {sac_nnc_nss_sistemas.shape[0]}')
        sac_nnc_nss_sistemas.to_excel(f'output/{self.dt}_e5_sac_nnc_nss_sistemas.xlsx', index= False)

def join(df_left, df_right, col_df_left, col_df_right, val_type):
    return df_left.merge(df_right, how = 'left', left_on = col_df_left, right_on = col_df_right, validate=val_type)


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
        res.loc[res[col].notna(), col] = res.loc[res[col].notna(), col].apply(unidecode)
        res.loc[res[col].notna(), col] = res.loc[res[col].notna(), col].str.replace(r'([^a-zA-Z0-9-+(). ])', '', regex=True)
        res.loc[res[col].notna(), col] = res.loc[res[col].notna(), col].str.strip()
        res.loc[res[col].notna(), col] = res.loc[res[col].notna(), col].str.upper()
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



def innit_commandline():
    conc = CONC()
    conc.run()


if __name__=='__main__':
    innit_commandline()
