<template>
    <v-container fluid>
        <v-toolbar color="white">
            <v-toolbar-title>{{dataset_name}}</v-toolbar-title>
            <v-spacer></v-spacer>
        </v-toolbar>
        <v-row>
            <v-col md="3">
                <v-dialog v-model="dialog" hide-overlay width="300">
                    <v-card color="primary" dark>
                        <v-card-text>
                            Please stand by
                            <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
                        </v-card-text>
                    </v-card>
                </v-dialog>
                <v-list
                    class="overflow-y-auto"
                    align="start"
                    justify="start"
                    dense
                    max-height="88vh"
                >
                    <v-container v-for="(item, idx) in tables" :key="idx">
                        <v-subheader v-if="item.header" :key="item.header" v-text="item.header"></v-subheader>

                        <v-divider v-else-if="item.divider" :key="index" :inset="item.inset"></v-divider>

                        <v-list-item
                            v-else
                            :key="item.table_name"
                            @click.stop="get_table_infos(item.project_name, item.dataset_name, item.table_name)"
                        >
                            <v-list-item-avatar>
                                <v-icon>mdi-table</v-icon>
                            </v-list-item-avatar>

                            <v-list-item-content>
                                <v-list-item-title>{{item.table_name}}({{item.nb_table}})</v-list-item-title>
                                <v-list-item-subtitle>Description: {{item.description}}</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>
                    </v-container>
                </v-list>
            </v-col>

            <v-col md="1">
                <v-divider vertical></v-divider>
            </v-col>

            <v-col md="8">
                <v-card
                    v-if="table_info_show"
                    align="start"
                    justify="start"
                    class="overflow-y-auto"
                    flat
                    max-height="88vh"
                >
                    <v-card-title>{{table_name}}</v-card-title>
                    <v-card-text>
                        <p class="text subtitle-2">Description:</p>
                        <p class="text-justify">{{table_infos[0]["description"]}}</p>
                        <Plotly
                            :data="graph_data_rows"
                            :layout="layout_rows"
                            :display-mode-bar="true"
                        ></Plotly>

                        <Plotly
                            :data="graph_data_size"
                            :layout="layout_size"
                            :display-mode-bar="true"
                        ></Plotly>

                        <v-select
                            :items="table_infos"
                            item-text="table_name"
                            label="Table name"
                            v-on:change="update_table_vue"
                        ></v-select>

                        <v-col class="text-center" md="6">
                            <v-text-field
                                v-model="search"
                                append-icon="mdi-magnify"
                                label="Search"
                                single-line
                                hide-details
                            ></v-text-field>
                        </v-col>

                        <v-data-table
                            :headers="headers"
                            :items="schema"
                            :loading="isLoading"
                            :search="search"
                            loading-text="Loading... Please wait"
                            item-key="field_name"
                            class="elevation-1"
                            hide-default-footer
                            :items-per-page="lengthSchema"
                        >
                            <template slot="items" slot-scope="props">
                                <td>{{ props.item.field_name }}</td>
                                <td class="text-xs-right">{{ props.item.field_type }}</td>
                                <td class="text-xs-right">{{ props.item.field_mode }}</td>
                                <td class="text-xs-right">{{ props.item.field_description }}</td>
                            </template>
                        </v-data-table>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { Plotly } from "vue-plotly";

export default {
    name: "Tables",
    components: {
        Plotly
    },

    created() {
        this.$store.dispatch("tables/getTables", [
            this.project_name,
            this.dataset_name,
            "true"
        ]);
        this.dialog = true;
        this.unsubscribe = this.$store.subscribe(mutation => {
            if (mutation.type === "tables/setTables") {
                this.tables = this.$store.state.tables.tables;
                this.dialog = false;
            }
        });
        if (this.clean_table_name) {
            this.get_table_infos(
                this.project_name,
                this.dataset_name,
                this.clean_table_name
            );
        }
    },
    computed: {
        table_infos() {
            return this.$store.state.table_infos.table_infos;
        },
        graph_data_rows() {
            return [
                {
                    x: this.labels,
                    y: this.num_rows,
                    type: "scatter"
                }
            ];
        },
        graph_data_size() {
            return [
                {
                    x: this.labels,
                    y: this.table_size,
                    type: "scatter"
                }
            ];
        }
    },
    methods: {
        get_table_infos(project_name, dataset_name, clean_table_name) {
            this.num_rows = [];
            this.table_size = [];
            this.labels = [];
            this.schema = [];
            this.$store.dispatch("table_infos/getTableInfos", [
                project_name,
                dataset_name,
                clean_table_name
            ]);
            this.table_info_show = false;

            this.unsubscribe = this.$store.subscribe(mutation => {
                if (mutation.type === "table_infos/setTableInfos") {
                    this.table_name = clean_table_name;
                    this.num_rows = this.$store.state.table_infos.num_rows;
                    this.table_size = this.$store.state.table_infos.table_size;
                    this.labels = this.$store.state.table_infos.labels;
                    this.table_info_show = true;
                    this.$router.push({
                        name: "Tables",
                        query: {
                            project_name: project_name,
                            dataset_name: dataset_name,
                            clean_table_name: clean_table_name
                        }
                    });
                    this.dialog = false;
                }
            });
            this.dialog = true;
        },
        update_table_vue(table) {
            this.isLoading = true;
            this.$store.dispatch("schema/getSchema", [
                this.project_name,
                this.dataset_name,
                table
            ]);

            this.unsubscribe = this.$store.subscribe(mutation => {
                if (mutation.type === "schema/setSchema") {
                    this.schema = this.$store.state.schema.schema;
                    this.isLoading = false;
                    this.lengthSchema = this.schema.length;
                }
            });
        }
    },
    data() {
        return {
            dialog: false,
            table_info_show: false,
            isLoading: false,
            project_name: this.$route.query.project_name,
            dataset_name: this.$route.query.dataset_name,
            clean_table_name: this.$route.query.clean_table_name,
            search: "",
            num_rows: [],
            table_size: [],
            tables: [],
            labels: [],
            schema: [
                {
                    field_name: "",
                    field_type: "",
                    field_mode: "",
                    field_description: ""
                }
            ],
            headers: [
                {
                    text: "Field name",
                    align: "start",
                    sortable: true,
                    value: "field_name"
                },
                { text: "Field type", value: "field_type", sortable: false },
                { text: "Field mode", value: "field_mode", sortable: false },
                {
                    text: "Field description",
                    value: "field_description",
                    sortable: false
                }
            ],
            lengthSchema: 0,
            layout_rows: {
                title: "Number of rows"
                // xaxis: { autorange: "reversed" }
            },
            layout_size: {
                title: "Size of tables"
                // xaxis: { autorange: "reversed" }
            }
        };
    }
};
</script>

<style scoped>
</style>