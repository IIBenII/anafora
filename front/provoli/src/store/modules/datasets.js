import axios from "axios";

// initial state
const state = {
    datasets: [],
    apiUrl: "http://172.17.0.1:5000/datasets"
}

// getters
const getters = {}

// actions
const actions = {
    async getRecipes({ state, commit }) {
        try {
            let response = await axios.get(`${state.apiUrl}`, {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }
            });
            commit("setRecipes", response.data.datasets);
        } catch (error) {
            commit("setRecipes", []);
        }
    }
}

// mutations
const mutations = {
    setRecipes(state, payload) {
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