<template>
    <!-- <v-card color="grey lighten-4" flat height="200px" tile> -->
    <nav>
        <!-- <v-app-bar color="primary" dark>
            <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>

            <v-toolbar-title>Anafora</v-toolbar-title>
        </v-app-bar>-->

        <v-navigation-drawer permanent app>
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title class="title">Anafora</v-list-item-title>
                    <v-list-item-subtitle>BigQuery data catalog</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>

            <v-divider></v-divider>

            <v-list dense nav>
                <v-list-item v-for="item in items" :key="item.title" link>
                    <v-list-item-icon>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-icon>

                    <v-list-item-content>
                        <v-list-item-title>{{ item.title }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
    </nav>
    <!-- </v-card> -->
</template>

<script>
export default {
    data() {
        return {
            items: [
                { title: "Home", icon: "mdi-view-dashboard" },
                { title: "About", icon: "mdi-help-box" }
            ],
            right: null
        };
    },
    name: "AppNavigation"
};
</script>

<style scoped>
</style>