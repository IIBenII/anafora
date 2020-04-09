import Vue from "vue";
import Vuex from "vuex";


import datasets from './modules/datasets'
import tables from './modules/tables'
import table_infos from './modules/table_infos'

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        datasets,
        tables,
        table_infos
    }
})