<template>
    <v-container grid-list-lg>
        <v-layout row wrap max-height="100%">
            <v-flex xs12 sm6 md6 lg4 v-for="(item, idx) in datasets" :key="idx">
                <v-card>
                    <v-card-text>
                        <div class="title">{{item.dataset_name}}</div>

                        <div class="subheading">Description: {{item.description}}</div>
                        <div class="subheading">Number of tables: {{item.nb_table}}</div>
                        <div class="subheading">Project: {{item.project_name}}</div>
                    </v-card-text>
                    <!-- <v-card-actions v-if="['menu'].includes($route.name)"> -->
                    <v-card-actions>
                        <v-btn
                            color="primary"
                            dark
                            :to="{path: '/tables', query: {project_name: item.project_name, dataset_name: item.dataset_name}}"
                        >More</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>

export default {
    name: "Datasets",

    created() {
        this.$store.dispatch("datasets/getDatasets");
    },
    computed: {
        datasets() {
            return this.$store.state.datasets.datasets;
        }
    },
    methods: {
    },
    data() {
        return {
            dialog: false,
            project_name: "",
            dataset_name: "",
            table_name: ""
        };
    }
};
</script>

<style scoped>
</style>