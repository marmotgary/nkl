
// This will ve using v-window and the v-window can take inside of it different items from pictures
<template>
  <v-carousel>
    <v-carousel-item v-for="(item,i) in items" :key="i" :src="item.src"></v-carousel-item>
  </v-carousel>
</template>

<script>
export default {
    data() {
        return {
            items: [
                {
                    src:
                        'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg'
                },
                {
                    src: 'https://cdn.vuetifyjs.com/images/carousel/sky.jpg'
                },
                {
                    src: 'https://cdn.vuetifyjs.com/images/carousel/planet.jpg'
                }
            ]
        };
    }
};
</script>
