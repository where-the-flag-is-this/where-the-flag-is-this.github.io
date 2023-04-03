<script setup lang="ts">
import "leaflet/dist/leaflet.css";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from '../stores/gameState';

const gameStateStore = useGameStateStore()
const { places } = storeToRefs(gameStateStore);

defineProps(['score'])

</script>

<template>
    <div class="flex flex-col pb-8">
        <h1 class="w-full flex justify-center text-4xl">Score</h1>
        <h3 class="w-full flex justify-center text-4xl">{{ score }} of {{ places.length }}</h3>
    </div>
</template>
