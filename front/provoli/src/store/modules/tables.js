import axios from "axios";

// initial state
const state = {
    tables: [],
    apiUrl: "http://172.17.0.1:5000/tables"
}

// getters
const getters = {}

// actions
const actions = {
    async getTables({ state, commit }, [project_name, dataset_name, compact]) {

        try {
            let response = await axios.get(`${state.apiUrl}`, {
                params: {
                    project_name: project_name,
                    dataset_name: dataset_name,
                    compact: compact
                },
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }
            });
            commit("setTables", response.data.tables);
        } catch (error) {
            commit("setTables", []);
        }
    }
}

// mutations
const mutations = {
    setTables(state, payload) {
        state.tables = payload;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}