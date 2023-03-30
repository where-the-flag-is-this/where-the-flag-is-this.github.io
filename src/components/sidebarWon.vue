<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { computed } from "vue";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from '../stores/gameState';

const gameStateStore = useGameStateStore()
const { currentIndex, gameState, places } = storeToRefs(gameStateStore);


const nextRound = () => {
    gameState.value = "newGame"
    currentIndex.value = 0
}

const score = computed(() => currentIndex.value + 1)

</script>

<template>
    <div class="flex flex-col justify-between h-full">
        <div class="flex flex-col pb-8">
            <h1 class="w-full flex justify-center text-4xl">Score</h1>
            <p class="w-full flex justify-center text-4xl">{{ score }}</p>
        </div>
        <div>
            YOU WON!!! You got all {{ places.length }} correct!
        </div>
        <button class="bg-green-500 rounded-full m-2 text-3xl p-2" @click="nextRound()">New Game</button>
    </div>
</template>
