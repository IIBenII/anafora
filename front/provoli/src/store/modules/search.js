import axios from "axios";

// initial state
const state = {
    search_datasets: [],
    search_tables: [],
    search_fields: [],
    apiUrl: process.env.VUE_APP_DATABASE_ADRESS + "/search"
}

// getters
const getters = {}

// actions
const actions = {
    async getSearch({ state, commit }, [search]) {
        try {
            let response = await axios.get(`${state.apiUrl}`, {
                params: {
                    filter: search,
                },
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }
            });
            commit("setSearch", response.data);
        } catch (error) {
            commit("setSearch", []);
        }
    }
}

// mutations
const mutations = {
    setSearch(state, payload) {
        state.search_datasets = payload.datasets;
        state.search_tables = payload.tables;
        state.search_fields = payload.fields;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}