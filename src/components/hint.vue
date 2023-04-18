<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { computed } from "vue";
import { storeToRefs } from 'pinia';
import { useGameStateStore } from '../stores/gameState';

const gameStateStore = useGameStateStore()
const { hintState} = storeToRefs(gameStateStore);

const hintAvailable = computed(() => hintState.value)
defineProps(['hint'])

</script>

<template>
    <div class="flex flex-col pb-8">
        <h5 v-if="hintAvailable" class="w-full flex justify-center text-4xl">{{ hint }}</h5>
    </div>
</template>
