gcons = {
    'input_path':'input/',
    'union_ss_aux' :['ss_ss_y', 'ss_n1_y', 'ss_n2_y', 'ss_n3_y', 'ss_tipo_y', 'ss_fcr_y', 'ss_estado_y', 'ss_subestado_y', 'ss_fecha_creacion_y', 'ss_fecha_solucion_y', 'ss_fecha_cierre_y', 'ss_tienda_origen_y', 'ss_orden_compra_y', 'ss_suborden_y', 'ss_num_f12_y', 'ss_area_problema_y', 'ss_sucursal_creador_y', 'ss_descripcion_y', 'ss_solucion_y'] ,
    'union_tes_ntc_aux' : ['tesoreria_ntc_cod aut nc_y', 'tesoreria_ntc_ss_y', 'tesoreria_ntc_valor de devolucion_y','tesoreria_ntc_tipo de devolucion_y', 'tesoreria_ntc_estado_y' ]
}

f11_vars = {
    'key': 'f11_nro_f11',
    'dkeys' : ['f11_nro_f11', 'f11_upc'], # TODO: validar duplicidad debería ser por F12 y UPC 
    'cnum' : ['f11_total_costo', 'f11_cant_prod'],
    'cstring' : [ 'f11_propietario', 'f11_nombre_local', 'f11_estado', 'f11_servicio'],
    'ckeep' : ['f11_nro_f11', 'f11_fecha_creacion' ,'f11_upc', 'f11_propietario', 'f11_cod_local', 
    'f11_nombre_local', 'f11_grupo', 'f11_estado', 'f11_servicio','f11_cant_prod', 'f11_total_costo','f11_observacion' ],
    'f11_f12':'f11_folio_f12',
    'upc_f11':'f11_upc',
    'observ_f11':'f11_observacion'
}

nc_vars = {
    'key':'nc_cautoriza',
    'dkeys':['nc_nfolio'], # TODO: validar duplicidad debería ser por F12 y UPC 
    'cnum':[],
    'cstring':[],
    'ckeep':['nc_cautoriza', 'nc_nfolio'],
    'f12':'nc_nfolio'
}

f12_vars = {
    'key':'f12_nfolio',
    'dkeys':['f12_nfolio', 'f12_prd_upc'],
    'cnum':['f12_qproducto','f12_mprecio', 'f12_mdescuento', 'f12_tprecio', 'f12_monto_nc'],
    'cstring':[],
    'ckeep' :['f12_nfolio', 'f12_loc_id', 'f12_loc_name', 'f12_dcreacion','f12_caja_venta','f12_secuencia_venta', 'f12_dreparto', 'f12_dpactada', 'f12_ctipo', 'f12_cvendedor', 'f12_bretira_dsp', 'f12_origin', 'f12_fpestado', 'f12_pestado', 'f12_fuestado', 'f12_desc_estado', 'f12_desc_subestado', 'f12_desc_mt', 'f12_username', 'f12_prd_upc', 'f12_prod_sku_id', 'f12_qproducto', 'f12_mprecio', 'f12_tprecio', 'f12_mdescuento', 'f12_dproceso', 'f12_loc_nc', 'f12_nterminal', 'f12_nsecuencia', 'f12_monto_nc', 'f12_cautoriza', 'f12_trn_tech_key', 'f12_origin_nc', 'f12_nsuborden','f12_ccomuna', 'f12_cmatrimonio', 'f12_ctipificacion' , 'f12_gco_inc_nc', 'f12_gco_ind_canal', 'f12_gco_ind_nc_inst', 'f12_gco_ind_gift_card', 'f12_gco_ind_te'],
    'estado':'f12_desc_estado', 
    'subestado':'f12_desc_subestado', 
    'mt':'f12_desc_mt', 
    'ind_fpactada':'gco_ind_fpactada', 
    'fpactada':'f12_dpactada',
    'nc':'f12_cautoriza',
    'so': 'f12_nsuborden',
    'folio': 'f12_nfolio',
    'upc':'f12_prd_upc'}

f3_vars = {
    'key': 'f3_nro_devolucion',
    'dkeys':['f3_folio_f12', 'f3_upc'],# TODO: validar duplicidad debería ser por F12 y UPC 
    'cnum':['f3_cantidad',  'f3_cant*costoprmd'],
    'cstring':['f3_nro_devolucion', 'f3_tipo_producto', 'f3_upc', 'f3_sku', 'f3_descripcion', 'f3_local', 'f3_descripcion5', 'f3_estado', 'f3_descripcion6','f3_folio_f12'],
    'ckeep':['f3_nro_devolucion', 'f3_fecha_reserva', 'f3_fecha_envio', 'f3_fecha_anulacion', 
    'f3_fecha_confirmacion','f3_tipo_producto', 'f3_upc', 'f3_sku', 'f3_descripcion', 'f3_local', 
    'f3_descripcion5', 'f3_estado', 'f3_descripcion6', 'f3_cantidad',  'f3_cant*costoprmd', 'f3_folio_f12'],
    'f3_f12':'f3_folio_f12',
    'upc_f3':'f3_upc'
}

siebel_vars = {
    'key': 'ss_ss',
    'dkeys':['ss_ss', 'ss_num_f12'],
    'cnum':[],
    'cstring':['ss_suborden','ss_n3', 'ss_num_f12'],
    'ckeep':['ss_ss','ss_n1','ss_n2','ss_n3','ss_tipo','ss_fcr','ss_estado','ss_subestado','ss_fecha_creacion','ss_fecha_solucion','ss_fecha_cierre',
    'ss_tienda_origen','ss_orden_compra','ss_suborden','ss_num_f12','ss_area_problema','ss_sucursal_creador','ss_descripcion','ss_solucion'],
    'n3':'ss_n3',
    'sorden':'ss_suborden',
    'ss_y':'ss_ss_y',
    'ss':'ss_ss',
    'f12':'ss_num_f12'

}

mc_vars = {
    'key': 'mc_entrada',
    'dkeys': ['mc_entrada'],
    'cstring' : ['mc_tip0_trabajo', 'mc_entrada'],
    'cnum' : [],
    'ckeep' : ['mc_tip0_trabajo', 'mc_entrada'],
    'entrada_mc':'mc_entrada'
}

q_vars = { 
    'key' : 'quiebres_f12',
    'dkeys' : ['quiebres_f12', 'quiebres_sku', 'quiebres_cantidad_cancelada'],
    'cnum' : ['quiebres_cost_unit_prod', 'quiebres_cantidad_cancelada'],
    'cstring': ['quiebres_tipo_quiebre'],
    'ckeep' : ['quiebres_f12', 'quiebres_sku', 'quiebres_cantidad_cancelada', 'quiebres_cost_unit_prod', 'quiebres_tipo_quiebre', 'quiebres_codigo_barras'],
    'f12_q':'quiebres_f12',
    'q_ean':'quiebres_codigo_barras'
}

q_man_vars = {
    'key' : 'q_man_f12',
    'dkeys' : ['q_man_f12', 'q_man_sku', 'q_man_unidades'],
    'cnum' : ['q_man_unidades'],
    'cstring' :[],
    'ckeep' : ['q_man_fecha del quiebre' ,'q_man_f12', 'q_man_sku', 'q_man_unidades'],
    'f12' : 'q_man_f12',
    'sku' : 'q_man_sku'
    }

ro_vars = {
    'key':'ro_ro',
    'dkeys':['ro_do_inicial',  'ro_upc'],
    'cnum':['ro_cantidad_producto'],
    'cstring':['ro_estado_ro'],
    'ckeep':[ 'ro_do_inicial',  'ro_upc', 'ro_fecha_creacion_ro',  'ro_ro', 'ro_estado_ro', 'ro_cantidad_producto'],
    'ro':'ro_ro',
    'do_inicial':'ro_do_inicial',
    'upc_ro':'ro_upc',
}

en_vars = {    
    'key':'en_centrada',
    'dkeys':['en_centrada'],
    'cnum':[ 'en_qcantida'],
    'cstring':['en_darticul' ],
    'ckeep':[ 'en_centrada','en_fcreareg', 'en_creferen', 'en_darticul',  'en_qcantida'],
    'centrada':'en_centrada'
}

tesor_nc = {
    'key':'tesoreria_ntc_cod aut nc',
    'dkeys':['tesoreria_ntc_cod aut nc'],
    'cnum':[ 'tesoreria_ntc_valor de devolucion'],
    'cstring':['tesoreria_ntc_estado' ],
    'ckeep':['tesoreria_ntc_cod aut nc', 'tesoreria_ntc_valor de devolucion', 'tesoreria_ntc_estado' ],
    'cod_aut':'tesoreria_ntc_cod aut nc',
    'estado':'tesoreria_ntc_estado',
    'ntc_ss':'tesoreria_ntc_ss',
    'ntc_ss_y':'tesoreria_ntc_ss_y'
}

tesor_sieb = {
    'key':'tesoreria_sieb_ss',
    'dkeys':['tesoreria_sieb_ss'],
    'cnum':[ 'tesoreria_sieb_valor de devolucion'],
    'cstring':['tesoreria_sieb_estado' ],
    'ckeep':['tesoreria_sieb_ss', 'tesoreria_sieb_valor de devolucion', 'tesoreria_sieb_estado' ],
    'sieb_ss':'tesoreria_sieb_ss',
    'estado_sieb':'tesoreria_sieb_estado'
}

pos_cyc= {'6': ['3'], 
        '35': ['13'], 
        '53': ['15'], 
        '60': ['46'], 
        '93': ['21'], 
        '96': ['22'], 
        '101': ['28'], 
        '123': ['47'], 
        '131': ['13'], 
        '183': ['38']}

pos_what = {'13': ['42'],
            '19': ['16'],
            '25': ['40'],
            '35': ['33'],
            '43': ['47'],
            '60': ['5'],
            '72': ['2'],
            '85': ['18'],
            '96': ['17'],
            '98': ['4'],
            '101': ['18'],
            '108': ['33']}
            
pos_sac = {'6': ['95'],
        '13': ['95'],
        '19': ['95'],
        '25': ['96'],
        '30': ['96'],
        '35': ['96'],
        '36': ['95'],
        '38': ['96'],
        '43': ['96'],
        '45': ['95'],
        '50': ['3'],
        '53': ['95'],
        '56': ['95'],
        '60': ['5','96'],
        '72': ['95'],
        '82': ['95'],
        '85': ['96', '97'],
        '93': ['95'],
        '96': ['96'],
        '98': ['96'],
        '101': ['95', '96'],
        '108': ['97'],
        '123': ['96'],
        '131': ['96'],
        '138': ['96'],
        '183': ['95', '96']}

tiendas = ['60',
'45',
'19',
'93',
'101',
'38',
'138',
'96',
'131',
'25',
'53',
'82',
'98',
'56',
'72',
'6',
'13',
'50',
'36',
'183',
'43',
'108',
'30',
'85',
'123',
'18',
'35']

columns_res_sac_nnt_nss = ['f12_nfolio',
 'f12_loc_id',
 'f12_loc_name',
 'f12_dcreacion',
 'f12_caja_venta',
 'f12_secuencia_venta',
 'f12_dreparto',
 'f12_dpactada',
 'f12_ctipo',
 'f12_cvendedor',
 'f12_bretira_dsp',
 'f12_origin',
 'f12_fpestado',
 'f12_pestado',
 'f12_fuestado',
 'f12_desc_estado',
 'f12_desc_subestado',
 'f12_desc_mt',
 'f12_username',
 'f12_prd_upc',
 'f12_qproducto',
 'f12_mprecio',
 'f12_tprecio',
 'f12_mdescuento',
 'f12_dproceso',
 'f12_loc_nc',
 'f12_nterminal',
 'f12_nsecuencia',
 'f12_monto_nc',
 'f12_cautoriza',
 'f12_trn_tech_key',
 'f12_origin_nc',
 'f12_nsuborden',
 'f12_gco_inc_nc',
 'f12_gco_ind_canal',
 'f12_gco_ind_nc_inst',
 'gco_ind_fpactada',
 'ss_ss',
 'ss_n1',
 'ss_n2',
 'ss_n3',
 'ss_tipo',
 'ss_fcr',
 'ss_estado',
 'ss_subestado',
 'ss_fecha_creacion',
 'ss_fecha_solucion',
 'ss_fecha_cierre',
 'ss_tienda_origen',
 'ss_orden_compra',
 'ss_suborden',
 'ss_num_f12',
 'ss_area_problema',
 'ss_sucursal_creador',
 'ss_descripcion',
 'ss_solucion',
 'tesoreria_ntc_cod aut nc',
 'tesoreria_ntc_ss',
 'tesoreria_ntc_valor de devolucion',
 'tesoreria_ntc_tipo de devolucion',
 'estado_tesoreria',
 'tesoreria_sieb_ss',
 'tesoreria_sieb_valor de devolucion',
 'tesoreria_sieb_tipo de devolucion',
 'tesoreria_sieb_estado',
 'ro_do_inicial',
 'ro_upc',
 'ro_fecha_creacion_ro',
 'ro_ro',
 'ro_estado_ro',
 'ro_cantidad_producto',
 'en_centrada',
 'en_fcreareg',
 'en_creferen',
 'en_darticul',
 'en_qcantida',
 'mc_tip0_trabajo',
 'mc_entrada',
 'f11_nro_f11',
 'f11_fecha_creacion',
 'f11_upc',
 'f11_propietario',
 'f11_cod_local',
 'f11_nombre_local',
 'f11_grupo',
 'f11_estado',
 'f11_servicio',
 'f11_cant_prod',
 'f11_total_costo',
 'f11_observacion',
 'f11_folio_f12',
 'f3_nro_devolucion',
 'f3_fecha_reserva',
 'f3_fecha_envio',
 'f3_fecha_anulacion',
 'f3_fecha_confirmacion',
 'f3_tipo_producto',
 'f3_upc',
 'f3_sku',
 'f3_descripcion',
 'f3_local',
 'f3_descripcion5',
 'f3_estado',
 'f3_descripcion6',
 'f3_cantidad',
 'f3_cant*costoprmd',
 'f3_folio_f12',
 'quiebres_f12',
 'quiebres_sku',
 'quiebres_cantidad_cancelada',
 'quiebres_cost_unit_prod',
 'quiebres_tipo_quiebre',
 'quiebres_codigo_barras',
 'gco_ind_pos',
 'gco_ind_entregas',
 'gco_ind_ss',
 'gco_ind_ss_n3',
 'gco_ind_btes',
 'gco_ind_registra_pago',
 'gco_comment',
 'comentarios_resp_rev',
 'Local usr cierre']