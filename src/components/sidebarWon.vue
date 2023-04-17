<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { computed } from "vue";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from '../stores/gameState';
import Score from "./score.vue"

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
        <Score :score="score" />
        <div>
            YOU WON!!! You got all {{ places.length }} correct!
        </div>
        <button class="button" @click="nextRound()">New Game</button>
    </div>
</template>
