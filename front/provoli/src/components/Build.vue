<template>
    <v-container>
        <v-row align="center">
            <v-col class="text-center" md="2">
                <!-- <div class="my-6"> -->
                <v-btn
                    color="primary"
                    @click.stop="build_datasets()"
                    :disabled="isDisabled"
                >Build dataset</v-btn>
                <!-- </div> -->
            </v-col>
            <v-col class="text-center" md="2">
                <v-btn
                    color="primary"
                    @click.stop="build_tables()"
                    :disabled="isDisabled"
                >Build tables</v-btn>
            </v-col>

            <v-col class="text-center" md="2">
                <v-btn
                    color="primary"
                    @click.stop="rowClick()"
                    :disabled="isDisabled"
                >Delete selected jobs</v-btn>
            </v-col>
            <v-col class="text-center" md="4">
                <v-progress-circular
                    indeterminate
                    color="primary"
                    v-if="this.$store.state.status.status == 'started'"
                ></v-progress-circular>
            </v-col>
        </v-row>
        <v-row>
            <v-col class="text-center" md="12">
                <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                ></v-text-field>
            </v-col>
        </v-row>
        <v-row>
            <v-col class="text-center" md="12">
                <v-data-table
                    v-model="selected"
                    :headers="headers"
                    :items="jobs"
                    :loading="isLoading"
                    :search="search"
                    loading-text="Loading... Please wait"
                    item-key="job_id"
                    show-select
                    class="elevation-1"
                >
                    <template v-slot:item.job_status="{ item }">
                        <v-chip :color="get_color(item.job_status)" dark>{{ item.job_status }}</v-chip>
                    </template>
                    <template slot="items" slot-scope="props">
                        <td>{{ props.item.job_id }}</td>
                        <td class="text-xs-right">{{ props.item.job_type }}</td>
                        <td class="text-xs-right">{{ props.item.job_start }}</td>
                        <td class="text-xs-right">{{ props.item.job_status }}</td>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    name: "Build",
    mounted: function() {
        window.setInterval(() => {
            this.get_build_datasets_status();
        }, 5000);
    },
    created() {
        this.get_build_datasets_status();
    },
    methods: {
        rowClick() {
            for (var i = 0; i < this.selected.length; i++) {
                console.log(this.selected[i].job_id);
                this.$store.dispatch("status/deleteStatus", [
                    this.selected[i].job_id
                ]);
            }
            this.get_build_datasets_status();
        },
        build_datasets() {
            this.$store.dispatch("build_datasets/postBuildDatasets");

            this.unsubscribe = this.$store.subscribe(mutation => {
                if (mutation.type === "build_datasets/setDatasets") {
                    this.get_build_datasets_status();
                }
            });
        },
        build_tables() {
            this.$store.dispatch("build_tables/postBuildTables");

            this.unsubscribe = this.$store.subscribe(mutation => {
                if (mutation.type === "build_tables/setTables") {
                    this.get_build_datasets_status();
                }
            });
        },
        get_build_datasets_status() {
            this.$store.dispatch("status/getStatus");

            this.unsubscribe = this.$store.subscribe(mutation => {
                if (mutation.type === "status/setStatus") {
                    this.jobs = this.$store.state.status.status;
                    this.isLoading = false;
                }
            });
        },
        get_color(status) {
            if (status == "failed") return "red";
            else if (status == "started") return "light-green accent-4";
            else if (status == "finished") return "green";
            else if (status == "queued") return "indigo";
            else if (status == "delete") return "grey";
            else return "orange";
        }
    },
    data() {
        return {
            isDisabled: false,
            isLoading: true,
            search: "",
            selected: [],
            jobs: [{ job_id: "", job_start: "", job_status: "", job_type: "" }],
            headers: [
                {
                    text: "Job id",
                    align: "start",
                    sortable: false,
                    value: "job_id"
                },
                { text: "job type", value: "job_type", sortable: true },
                { text: "job start", value: "job_start", sortable: true },
                { text: "job status", value: "job_status", sortable: true }
            ]
        };
    }
};
</script>>

<style scoped>
</style>