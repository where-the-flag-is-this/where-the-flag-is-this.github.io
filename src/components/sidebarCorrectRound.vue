<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { computed } from "vue";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from '../stores/gameState';
import Score from "./score.vue"

const gameStateStore = useGameStateStore()
const { currentIndex, gameState, currentPlace, places } = storeToRefs(gameStateStore);


const nextRound = () => {
    gameState.value = "ongoingRound"
    currentIndex.value++
}

const score = computed(() => currentIndex.value + 1)

</script>

<template>
    <div class="flex flex-col justify-between h-full">
        <Score :score="score" />
        <div>
            Correct! It was <b>{{ currentPlace.properties.countryLabel }}</b>
        </div>
        <button class="button" @click="nextRound()">Next round</button>
    </div>
</template>
