<template>
    <nav>
        <v-navigation-drawer permanent app>
            <v-list-item>
                <v-list-item-content>
                    <v-list-item-title class="title">Anafora</v-list-item-title>
                    <v-list-item-subtitle>BigQuery data catalog</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>

            <v-divider></v-divider>

            <v-list dense nav>
                <v-list-item v-for="item in items" :key="item.title" :to="item.link" link>
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
                { title: "Home", icon: "mdi-view-dashboard", link: "/" },
                { title: "Build", icon: "mdi-wrench", link: "/build" }
            ],
            right: null
        };
    },
    name: "AppNavigation"
};
</script>

<style scoped>
</style>