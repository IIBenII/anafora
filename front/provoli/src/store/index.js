import Vue from "vue";
import Vuex from "vuex";


import datasets from './modules/datasets'
import tables from './modules/tables'
import table_infos from './modules/table_infos'

import build_datasets from './modules/build_datasets'
import build_tables from './modules/build_tables'
import status from './modules/status'


Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        datasets,
        tables,
        table_infos,
        build_datasets,
        build_tables,
        status
    }
})