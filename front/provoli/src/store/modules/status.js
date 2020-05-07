import axios from "axios";

// initial state
const state = {
    status: [],
    apiUrl: process.env.VUE_APP_WORKER_ADRESS + "/jobs"
}

// getters
const getters = {}

// actions
const actions = {
    async getStatus({ state, commit }) {
        try {
            let response = await axios.get(`${state.apiUrl}`, {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }
            });
            commit("setStatus", response.data.jobs);
        } catch (error) {
            commit("setStatus", []);
        }
    },

    async deleteStatus({ state, commit }, [job_id]) {
        try {
            let response = await axios.delete(`${state.apiUrl}/${job_id}`, {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }
            });
            commit("delStatus", response.data);
        } catch (error) {
            commit("delStatus", []);
        }
    }
}

// mutations
const mutations = {
    setStatus(state, payload) {
        state.status = payload;
    },
    delStatus(state, payload) {
        console.log(payload);
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}