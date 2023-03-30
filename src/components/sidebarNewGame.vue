<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { computed } from "vue";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from '../stores/gameState';

const gameStateStore = useGameStateStore()
const { currentIndex, gameState } = storeToRefs(gameStateStore);
const { shuffleAllPlaces } = gameStateStore


const startGame = () => {
    gameState.value = "ongoingRound"
    shuffleAllPlaces()
    currentIndex.value = 0
}

const score = computed(() => currentIndex.value)

</script>

<template>
    <div class="flex flex-col justify-between h-full">
        <div class="flex flex-col pb-8">
            <h1 class="w-full flex justify-center text-4xl">Score</h1>
            <h3 class="w-full flex justify-center text-4xl">{{ score }}</h3>
        </div>
        <div>
            <p>
                You will get a flag of a place. Guess where it is on the map an hit 'Guess'.
                The locations are from WikiData and linked to active jurisdiction not claims!
            </p>
        </div>
        <button class="bg-green-500 rounded-full m-2 text-3xl p-2" @click="startGame()">Start Game</button>
    </div>
</template>
