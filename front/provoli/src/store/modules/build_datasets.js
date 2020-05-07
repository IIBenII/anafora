import axios from "axios";

// initial state
const state = {
    build_datasets: [],
    apiUrl: process.env.VUE_APP_WORKER_ADRESS + "/datasets"
}

// getters
const getters = {}

// actions
const actions = {
    async postBuildDatasets({ state, commit }) {
        try {
            let response = await axios.post(`${state.apiUrl}`, {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }
            });
            commit("setDatasets", response.data);
        } catch (error) {
            commit("setDatasets", []);
        }
    }
}

// mutations
const mutations = {
    setDatasets(state, payload) {
        state.build_datasets = payload;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}