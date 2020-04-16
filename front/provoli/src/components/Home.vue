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
                            @click.stop="open_dialog(item.project_name,item.dataset_name)"
                        >More</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
        <v-row justify="center">
            <v-dialog v-model="dialog2" hide-overlay width="300">
                <v-card color="primary" dark>
                    <v-card-text>
                        Please stand by
                        <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
                    </v-card-text>
                </v-card>
            </v-dialog>
            <v-dialog
                v-model="dialog"
                fullscreen
                hide-overlay
                transition="dialog-bottom-transition"
            >
                <v-card>
                    <v-toolbar dark color="primary">
                        <v-btn icon dark @click="close_dialog()">
                            <v-icon>mdi-close</v-icon>
                        </v-btn>
                        <v-toolbar-title>{{dataset_name}}</v-toolbar-title>
                        <v-spacer></v-spacer>
                    </v-toolbar>
                    <v-row no-gutters>
                        <v-col>
                            <v-subheader>Tables:</v-subheader>
                        </v-col>
                    </v-row>
                    <v-row no-gutters>
                        <v-col md="4">
                            <v-list class="overflow-y-auto" max-height="80vh" dense>
                                <v-container v-for="(item, idx) in tables" :key="idx">
                                    <v-subheader
                                        v-if="item.header"
                                        :key="item.header"
                                        v-text="item.header"
                                    ></v-subheader>

                                    <v-divider
                                        v-else-if="item.divider"
                                        :key="index"
                                        :inset="item.inset"
                                    ></v-divider>

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

                        <v-col md="8">
                            <v-card
                                v-if="table_info_show"
                                class="overflow-y-auto"
                                flat
                                max-height="80vh"
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
                                        label="Table name:"
                                        solo
                                        v-on:change="update_table_vue"
                                        v-model="table_infos[0]"
                                    ></v-select>
                                    <p class="text-justify">
                                        Morbi mattis ullamcorper velit. Donec orci lectus, aliquam ut, faucibus non, euismod id, nulla. Fusce convallis metus id felis luctus adipiscing. Aenean massa. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus.
                                        Nulla consequat massa quis enim. Praesent venenatis metus at tortor pulvinar varius. Donec venenatis vulputate lorem. Phasellus accumsan cursus velit. Pellentesque ut neque.
                                    </p>
                                    <p class="text-justify">
                                        Morbi mattis ullamcorper velit. Donec orci lectus, aliquam ut, faucibus non, euismod id, nulla. Fusce convallis metus id felis luctus adipiscing. Aenean massa. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus.
                                        Nulla consequat massa quis enim. Praesent venenatis metus at tortor pulvinar varius. Donec venenatis vulputate lorem. Phasellus accumsan cursus velit. Pellentesque ut neque.
                                    </p>
                                    <p class="text-justify">
                                        Morbi mattis ullamcorper velit. Donec orci lectus, aliquam ut, faucibus non, euismod id, nulla. Fusce convallis metus id felis luctus adipiscing. Aenean massa. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus.
                                        Nulla consequat massa quis enim. Praesent venenatis metus at tortor pulvinar varius. Donec venenatis vulputate lorem. Phasellus accumsan cursus velit. Pellentesque ut neque.
                                    </p>
                                    <p class="text-justify">
                                        Morbi mattis ullamcorper velit. Donec orci lectus, aliquam ut, faucibus non, euismod id, nulla. Fusce convallis metus id felis luctus adipiscing. Aenean massa. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus.
                                        Nulla consequat massa quis enim. Praesent venenatis metus at tortor pulvinar varius. Donec venenatis vulputate lorem. Phasellus accumsan cursus velit. Pellentesque ut neque.
                                    </p>
                                    <p class="text-justify">
                                        Morbi mattis ullamcorper velit. Donec orci lectus, aliquam ut, faucibus non, euismod id, nulla. Fusce convallis metus id felis luctus adipiscing. Aenean massa. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus.
                                        Nulla consequat massa quis enim. Praesent venenatis metus at tortor pulvinar varius. Donec venenatis vulputate lorem. Phasellus accumsan cursus velit. Pellentesque ut neque.
                                    </p>
                                    <p class="text-justify">
                                        Morbi mattis ullamcorper velit. Donec orci lectus, aliquam ut, faucibus non, euismod id, nulla. Fusce convallis metus id felis luctus adipiscing. Aenean massa. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus.
                                        Nulla consequat massa quis enim. Praesent venenatis metus at tortor pulvinar varius. Donec venenatis vulputate lorem. Phasellus accumsan cursus velit. Pellentesque ut neque.
                                    </p>
                                    <p class="text-justify">
                                        Morbi mattis ullamcorper velit. Donec orci lectus, aliquam ut, faucibus non, euismod id, nulla. Fusce convallis metus id felis luctus adipiscing. Aenean massa. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus.
                                        Nulla consequat massa quis enim. Praesent venenatis metus at tortor pulvinar varius. Donec venenatis vulputate lorem. Phasellus accumsan cursus velit. Pellentesque ut neque.
                                    </p>
                                    <p class="text-justify">
                                        Morbi mattis ullamcorper velit. Donec orci lectus, aliquam ut, faucibus non, euismod id, nulla. Fusce convallis metus id felis luctus adipiscing. Aenean massa. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus.
                                        Nulla consequat massa quis enim. Praesent venenatis metus at tortor pulvinar varius. Donec venenatis vulputate lorem. Phasellus accumsan cursus velit. Pellentesque ut neque.
                                    </p>
                                    <p class="text-justify">
                                        Morbi mattis ullamcorper velit. Donec orci lectus, aliquam ut, faucibus non, euismod id, nulla. Fusce convallis metus id felis luctus adipiscing. Aenean massa. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus.
                                        Nulla consequat massa quis enim. Praesent venenatis metus at tortor pulvinar varius. Donec venenatis vulputate lorem. Phasellus accumsan cursus velit. Pellentesque ut neque.
                                    </p>
                                </v-card-text>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-card>
            </v-dialog>
        </v-row>
    </v-container>
</template>

<script>
import { Plotly } from "vue-plotly";

export default {
    name: "GlobalViews",
    components: {
        Plotly
    },

    created() {
        this.$store.dispatch("datasets/getDatasets");
    },
    computed: {
        datasets() {
            return this.$store.state.datasets.datasets;
        },
        tables() {
            return this.$store.state.tables.tables;
        },
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
        close_dialog() {
            this.num_rows = [];
            this.table_size = [];
            this.labels = [];
            this.table_info_show = false;
            this.$store.state.table_infos.table_infos = [];
            this.dialog = false;
        },
        open_dialog(project_name, dataset_name) {
            this.$store.dispatch("tables/getTables", [
                project_name,
                dataset_name,
                "true"
            ]);
            this.unsubscribe = this.$store.subscribe(mutation => {
                if (mutation.type === "tables/setTables") {
                    this.dialog = true;
                    this.dialog2 = false;
                    this.dataset_name = dataset_name;
                }
            });
            this.dialog2 = true;
        },
        get_table_infos(project_name, dataset_name, clean_table_name) {
            this.num_rows = [];
            this.table_size = [];
            this.labels = [];
            this.$store.dispatch("table_infos/getTableInfos", [
                project_name,
                dataset_name,
                clean_table_name
            ]);

            this.unsubscribe = this.$store.subscribe(mutation => {
                if (mutation.type === "table_infos/setTableInfos") {
                    this.table_name = clean_table_name;
                    this.num_rows = this.$store.state.table_infos.num_rows;
                    this.table_size = this.$store.state.table_infos.table_size;
                    this.labels = this.$store.state.table_infos.labels;
                    this.table_info_show = true;
                    this.dialog2 = false;
                }
            });
            this.dialog2 = true;
        },
        update_table_vue(table) {
            this.num_rows_table = this.$store.state.table_infos.table_infos_dict[
                table
            ].num_rows;

            this.table_size_table = this.$store.state.table_infos.table_infos_dict[
                table
            ].table_size;
            console.log(this.num_rows_table);
        }
    },
    data() {
        return {
            dialog: false,
            dialog2: false,
            table_info_show: false,
            dataset_name: "",
            table_name: "",
            num_rows: [],
            table_size: [],
            labels: [],
            layout_rows: {
                title: "Number of rows",
                // xaxis: { autorange: "reversed" }
            },
            layout_size: {
                title: "Size of tables",
                // xaxis: { autorange: "reversed" }
            }
        };
    }
};
</script>

<style scoped>
</style>