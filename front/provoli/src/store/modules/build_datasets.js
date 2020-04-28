import axios from "axios";

// initial state
const state = {
    build_datasets: [],
    apiUrl: "http://172.17.0.1:5001/datasets"
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