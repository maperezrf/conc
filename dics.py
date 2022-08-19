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
    'f11_nombre_local', 'f11_grupo', 'f11_estado', 'f11_servicio','f11_cant_prod', 'f11_total_costo','f11_observacion' ]
}

nc_vars = {
    'key':'nc_cautoriza_nc',
    'dkeys':['nc_nfolio', 'nc_prod_ean_id'], # TODO: validar duplicidad debería ser por F12 y UPC 
    'cnum':['nc_qcantidad', 'nc_monto_sku_nc'],
    'cstring':['nc_estado_nc', 'nc_local_v_nc'],
    'ckeep':['nc_cautoriza_nc', 'nc_sku', 'nc_qcantidad', 'nc_monto_sku_nc', 'nc_estado_nc', 'nc_local_v_nc', 'nc_nfolio', 'nc_prod_ean_id']
}

f12_vars = {
    'key':'f12_nfolio',
    'dkeys':['f12_nfolio', 'f12_prd_upc'],
    'cnum':['f12_qproducto','f12_mprecio'],
    'cstring':['f12_loc_name','f12_desc_estado','f12_desc_subestado','f12_desc_mt','f12_ind_nc', 'f12_so'],
    'ckeep':['f12_nfolio','f12_loc_id','f12_loc_name','f12_dcreacion','f12_dreparto','f12_dpactada','f12_desc_estado',
    'f12_desc_subestado','f12_desc_mt','f12_ind_nc','f12_ctipo','f12_cvendedor','f12_bretira_dsp','f12_partition_date',
    'f12_origin','f12_prd_upc','f12_qproducto','f12_mprecio', 'f12_so'],
    'estado':'f12_desc_estado',
    'subestado':'f12_desc_subestado',
    'mt':'f12_desc_mt',
    'ind_fpactada':'gco_ind_fpactada',
    'fpactada':'f12_dpactada'

}

f3_vars = {
    'key': 'f3_nro_devolucion',
    'dkeys':['f3_folio_f12', 'f3_upc'],# TODO: validar duplicidad debería ser por F12 y UPC 
    'cnum':['f3_cantidad',  'f3_cant*costoprmd'],
    'cstring':['f3_nro_devolucion', 'f3_tipo_producto', 'f3_upc', 'f3_sku', 'f3_descripcion', 'f3_local', 'f3_descripcion5', 'f3_estado', 'f3_descripcion6','f3_folio_f12'],
    'ckeep':['f3_nro_devolucion', 'f3_fecha_reserva', 'f3_fecha_envio', 'f3_fecha_anulacion', 
    'f3_fecha_confirmacion','f3_tipo_producto', 'f3_upc', 'f3_sku', 'f3_descripcion', 'f3_local', 
    'f3_descripcion5', 'f3_estado', 'f3_descripcion6', 'f3_cantidad',  'f3_cant*costoprmd', 'f3_folio_f12']
}

siebel_vars = {
    'key': 'ss_suborden',
    'dkeys':['ss_suborden'],
    'cnum':[],
    'cstring':['ss_suborden','ss_n3', 'ss_num_f12'],
    'ckeep':['ss_ss','ss_n1','ss_n2','ss_n3','ss_tipo','ss_fcr','ss_estado','ss_subestado','ss_fecha_creacion','ss_fecha_solucion','ss_fecha_cierre',
    'ss_tienda_origen','ss_orden_compra','ss_suborden','ss_num_f12','ss_area_problema','ss_sucursal_creador','ss_descripcion','ss_solucion']
}

mc_vars = {
    'key': 'mc_entrada',
    'dkeys': ['mc_entrada'],
    'cstring' : ['mc_tip0_trabajo', 'mc_entrada'],
    'cnum' : [],
    'ckeep' : ['mc_tip0_trabajo', 'mc_entrada']
}

q_vars = { 
    'key' : 'quiebres_f12',
    'dkeys' : ['quiebres_f12', 'quiebres_sku', 'quiebres_cantidad_cancelada'],
    'cnum' : ['quiebres_cost_unit_prod', 'quiebres_cantidad_cancelada'],
    'cstring': ['quiebres_tipo_quiebre'],
    'ckeep' : ['quiebres_f12', 'quiebres_sku', 'quiebres_cantidad_cancelada', 'quiebres_cost_unit_prod', 'quiebres_tipo_quiebre', 'quiebres_codigo_barras']
}

ro_vars = {
    'key':'ro_ro',
    'dkeys':['ro_do_inicial',  'ro_upc'],
    'cnum':['ro_cantidad_producto'],
    'cstring':['ro_estado_ro'],
    'ckeep':[ 'ro_do_inicial',  'ro_upc', 'ro_fecha_creacion_ro',  'ro_ro', 'ro_estado_ro', 'ro_cantidad_producto']
}

en_vars = {    
    'key':'en_centrada',
    'dkeys':['en_centrada'],
    'cnum':[ 'en_qcantida'],
    'cstring':['en_darticul' ],
    'ckeep':[ 'en_centrada','en_fcreareg', 'en_creferen', 'en_darticul',  'en_qcantida']
}

tesor_nc = {
    'key':'tesoreria_ntc_cod aut nc',
    'dkeys':['tesoreria_ntc_cod aut nc'],
    'cnum':[ 'tesoreria_ntc_valor de devolucion'],
    'cstring':['tesoreria_ntc_tipo de devolucion', 'tesoreria_ntc_estado' ],
    'ckeep':['tesoreria_ntc_cod aut nc', 'tesoreria_ntc_ss', 'tesoreria_ntc_valor de devolucion','tesoreria_ntc_tipo de devolucion', 'tesoreria_ntc_estado' ]
}

tesor_sieb = {
    'key':'tesoreria_sieb_ss',
    'dkeys':['tesoreria_sieb_ss'],
    'cnum':[ 'tesoreria_sieb_valor de devolucion'],
    'cstring':['tesoreria_sieb_tipo de devolucion', 'tesoreria_sieb_estado' ],
    'ckeep':['tesoreria_sieb_ss', 'tesoreria_sieb_valor de devolucion','tesoreria_sieb_tipo de devolucion', 'tesoreria_sieb_estado' ]
}