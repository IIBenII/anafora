<template>
    <v-container fill-height fluid>
        <v-row justify="center" align="center">
            <v-col class="text-center" md="10">
                <v-form action="/search">
                    <v-text-field
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Search"
                        single-line
                        hide-details
                        name="search"
                        required
                    ></v-text-field>
                </v-form>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    name: "home",
    methods: {
        submit() {
            this.nativeForm.submit();
        }
    }
};
</script>

<style scoped>
</style>