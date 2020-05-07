import axios from "axios";

// initial state
const state = {
    build_tables: [],
    apiUrl: process.env.VUE_APP_WORKER_ADRESS + "/tables"
}

// getters
const getters = {}

// actions
const actions = {
    async postBuildTables({ state, commit }) {
        try {
            let response = await axios.post(`${state.apiUrl}`, {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }
            });
            commit("setTables", response.data);
        } catch (error) {
            commit("setTables", []);
        }
    }
}

// mutations
const mutations = {
    setTables(state, payload) {
        state.build_tables = payload;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}