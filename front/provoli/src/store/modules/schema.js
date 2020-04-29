import axios from "axios";

// initial state
const state = {
    schema: [],
    apiUrl: "http://172.17.0.1:5000/schema"
}

// getters
const getters = {}

// actions
const actions = {
    async getSchema({ state, commit }, [project_name, dataset_name, table_name]) {

        try {
            let response = await axios.get(`${state.apiUrl}`, {
                params: {
                    project_name: project_name,
                    dataset_name: dataset_name,
                    table_name: table_name
                },
                headers: {
                    'Access-Control-Allow-Origin': '*',
                }
            });
            commit("setSchema", response.data.schema);
        } catch (error) {
            commit("setSchema", []);
        }
    }
}

// mutations
const mutations = {
    setSchema(state, payload) {
        state.schema = payload;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}