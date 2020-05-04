<template>
    <v-container fluid>
        <v-app-bar color="white" absolute elevate-on-scroll scroll-target="#scrolling-techniques-7">
            <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                @keyup.enter="search_func"
                @click:append="search_func"
                @input="search_func"
                label="Search"
                single-line
                hide-details
            ></v-text-field>
        </v-app-bar>

        <v-row>
            <v-card color="transparent" height="40" v-if="this.search !== undefined"></v-card>
        </v-row>

        <v-sheet
            id="scrolling-techniques-7"
            align="baseline"
            class="overflow-y-auto"
            max-height="93vh"
            width="100%"
            v-if="this.search !== undefined"
        >
            <v-col class="text-center" md="12">
                <v-card outlined>
                    <v-card-title>Dataset:</v-card-title>
                    <v-data-table
                        :headers="headers_datasets"
                        :items="search_datasets"
                        :loading="isLoading"
                        :items-per-page="lengthTables"
                        loading-text="Loading... Please wait"
                    >
                        <template slot="items" slot-scope="props">
                            <td>{{ props.item.project_name }}</td>
                            <td class="text-xs-right">{{ props.item.dataset_name }}</td>
                            <td class="text-xs-right">{{ props.item.description }}</td>
                        </template>
                    </v-data-table>
                </v-card>
            </v-col>

            <v-col class="text-center" md="12">
                <v-card outlined>
                    <v-card-title>Tables:</v-card-title>
                    <v-data-table
                        :headers="headers_tables"
                        :items="search_tables"
                        :loading="isLoading"
                        :items-per-page="lengthTables"
                        loading-text="Loading... Please wait"
                    >
                        <template slot="items" slot-scope="props">
                            <td>{{ props.item.project_name }}</td>
                            <td class="text-xs-right">{{ props.item.dataset_name }}</td>
                            <td class="text-xs-right">{{ props.item.table_name }}</td>
                            <td class="text-xs-right">{{ props.item.description }}</td>
                        </template>
                    </v-data-table>
                </v-card>
            </v-col>

            <v-col class="text-center" md="12">
                <v-card outlined>
                    <v-card-title>Field:</v-card-title>
                    <v-data-table
                        :headers="headers_fields"
                        :items="search_fields"
                        :loading="isLoading"
                        :items-per-page="lengthTables"
                        loading-text="Loading... Please wait"
                    >
                        <template slot="items" slot-scope="props">
                            <td>{{ props.item.project_name }}</td>
                            <td class="text-xs-right">{{ props.item.dataset_name }}</td>
                            <td class="text-xs-right">{{ props.item.table_name }}</td>
                            <td class="text-xs-right">{{ props.item.description }}</td>
                        </template>
                    </v-data-table>
                </v-card>
            </v-col>
        </v-sheet>
    </v-container>
</template>


<script>
export default {
    name: "Search",
    created() {
        this.search_func();
    },
    methods: {
        search_func() {
            this.last_hit = this.search;
            if (this.locked == false) {
                this.locked = true;
                this.current_hit = this.search;
                this.$store.dispatch("search/getSearch", [this.search]);
                this.isLoading = true;
                this.unsubscribe = this.$store.subscribe(mutation => {
                    if (mutation.type === "search/setSearch") {
                        this.isLoading = false;
                        this.search_tables = this.$store.state.search.search_tables;
                        this.search_datasets = this.$store.state.search.search_datasets;
                        this.search_fields = this.$store.state.search.search_fields;
                        // this.lengthDatasets = this.datasets.length;
                        this.locked = false;
                        if (this.last_hit != this.current_hit) {
                            this.search_func();
                        }
                    }
                });
            }
        }
    },
    data() {
        return {
            search: this.$route.query.search,
            last_hit: "",
            current_hit: "",
            locked: false,
            lengthDatasets: 10,
            lengthTables: 10,
            isLoading: false,
            search_datasets: [
                {
                    project_name: "",
                    dataset_name: "",
                    description: ""
                }
            ],
            search_tables: [
                {
                    project_name: "",
                    dataset_name: "",
                    table_name: "",
                    description: ""
                }
            ],
            search_fields: [
                {
                    project_name: "",
                    dataset_name: "",
                    table_name: "",
                    field_name: "",
                    field_mode: "",
                    field_type: "",
                    field_description: ""
                }
            ],
            headers_datasets: [
                {
                    text: "Project name",
                    align: "start",
                    sortable: true,
                    value: "project_name"
                },
                { text: "Dataset name", value: "dataset_name", sortable: true },
                {
                    text: "Dataset description",
                    value: "description",
                    sortable: true
                }
            ],
            headers_tables: [
                {
                    text: "Project name",
                    align: "start",
                    sortable: true,
                    value: "project_name"
                },
                { text: "Dataset name", value: "dataset_name", sortable: true },
                { text: "Table name", value: "table_name", sortable: true },
                {
                    text: "Table description",
                    value: "description",
                    sortable: true
                }
            ],
            headers_fields: [
                {
                    text: "Project name",
                    align: "start",
                    sortable: true,
                    value: "project_name"
                },
                { text: "Dataset name", value: "dataset_name", sortable: true },
                { text: "Table name", value: "table_name", sortable: true },
                { text: "Field name", value: "field_name", sortable: true },
                { text: "Field mode", value: "field_mode", sortable: true },
                { text: "Field type", value: "field_type", sortable: true },
                {
                    text: "Field description",
                    value: "field_description",
                    sortable: true
                }
            ]
        };
    }
};
</script>>

<style scoped>
</style>