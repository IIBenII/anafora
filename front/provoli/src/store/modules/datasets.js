import axios from "axios";

// initial state
const state = {
    datasets: [],
    apiUrl: process.env.VUE_APP_DATABASE_ADRESS + "/datasets"
}

// getters
const getters = {}

// actions
const actions = {
    async getDatasets({ state, commit }) {
        try {
            let response = await axios.get(`${state.apiUrl}`, {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }
            });
            commit("setDatasets", response.data.datasets);
        } catch (error) {
            commit("setDatasets", []);
        }
    }
}

// mutations
const mutations = {
    setDatasets(state, payload) {
        state.datasets = payload;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}