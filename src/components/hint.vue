<script setup lang="ts">
import "leaflet/dist/leaflet.css";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from '../stores/gameState';

const gameStateStore = useGameStateStore()
const { places } = storeToRefs(gameStateStore);

defineProps(['hint'])

</script>

<template>
    <div class="flex flex-col pb-8">
        <h5 class="w-full flex justify-center text-4xl">{{ hint }}</h5>
    </div>
</template>
