<template>
    <span>
        <banner></banner>
        <lorem-ipsum></lorem-ipsum>
    </span>
</template>

<script>
import Banner from '@/components/Banner';
import LoremIpsum from '@/components/LoremIpsum';

export default {
    name: 'home',
    components: {
        Banner,
        LoremIpsum
    }
};
</script>
