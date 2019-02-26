<template>
    <v-container fluid fill-height class="banner" style="max-height:100vh;">
        <v-layout justify-center align-center column pa-5>
            <div class="display-4 font-weight-black white--text text-xs-center">
                THIS IS THE SITE OF
            </div>
            <div
                class="display-4 font-weight-black white--text text-xs-center mb-3"
            >
                NATIONAALI KYYKKÄ LIIGA
            </div>
            <div class="display-1 font-weight-bold white--text text-xs-center">
                Typerä ja lapsellinen peli.
            </div>
        </v-layout>
    </v-container>
</template>

<script>
export default {
    name: 'Banner'
};
</script>

<style scoped>
.banner {
    background: url('http://source.unsplash.com/CCxWLAx0qmk');
    background-size: cover;
    width: 100%;
    height: 100%;
}
</style>
