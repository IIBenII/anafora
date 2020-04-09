import axios from "axios";

// initial state
const state = {
    table_infos: [],
    table_infos_dict: {},
    num_rows: [],
    table_size: [],
    labels: [],
    apiUrl: "http://172.17.0.1:5000/table_infos"
}

// getters
const getters = {}

// actions
const actions = {
    async getTableInfos({ state, commit }, [project_name, dataset_name, clean_table_name]) {

        try {
            let response = await axios.get(`${state.apiUrl}`, {
                params: {
                    project_name: project_name,
                    dataset_name: dataset_name,
                    clean_table_name: clean_table_name
                },
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }
            });
            commit("setTableInfos", response.data.table_infos);
        } catch (error) {
            commit("setTableInfos", []);
        }
    }
}

// mutations
const mutations = {
    setTableInfos(state, payload) {
        state.table_infos = payload;
        state.num_rows = []
        state.labels = []
        state.table_size = []

        for (var elt in payload) {
            state.table_infos_dict[payload[elt].table_name] = {
                "num_rows": payload[elt].num_rows,
                "table_size": payload[elt].table_size
            }
            state.num_rows.push(payload[elt].num_rows)
            state.table_size.push(payload[elt].table_size)

            var table_name = payload[elt].table_name
            var table_name_split = table_name.split("_")
            var date_yyyymmdd = table_name_split[table_name_split.length - 1]
            var year = date_yyyymmdd.substring(0, 4)
            var month = date_yyyymmdd.substring(4, 6)
            var day = date_yyyymmdd.substring(6, 8)
            state.labels.push(year + "-" + month + "-" + day)
        }
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}