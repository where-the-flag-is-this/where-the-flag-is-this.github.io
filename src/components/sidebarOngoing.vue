<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { computed } from "vue";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from '../stores/gameState';
import Score from "./score.vue"
import Hint from "./hint.vue"


const gameStateStore = useGameStateStore()
const { places, currentIndex, gameState,hintState,  markerPosition } = storeToRefs(gameStateStore);


const currentPlace = computed(() => places.value[currentIndex.value])

function pointInPolygon(x: number, y: number, polyPoints: Array<Array<number>>) {
    let inside = false;
    for (var i = 0, j = polyPoints.length - 1; i < polyPoints.length; j = i++) {
        var xi = polyPoints[i][0], yi = polyPoints[i][1];
        var xj = polyPoints[j][0], yj = polyPoints[j][1];
        if (((yi > y) != (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) {
            inside = !inside
        }
    }

    return inside;
}
function isMarkerInsidePolygon() {
    const x = markerPosition.value.lng, y = markerPosition.value.lat;
    if (currentPlace.value.geometry.type == "Polygon") {
        const polyPoints = currentPlace.value.geometry.coordinates[0];
        return pointInPolygon(x, y, polyPoints)
    } else if (currentPlace.value.geometry.type == "MultiPolygon") {
        for (var i = 0; i < currentPlace.value.geometry.coordinates.length; i++) {
            const polyPoints = currentPlace.value.geometry.coordinates[i][0];
            if (pointInPolygon(x, y, polyPoints)) {
                return true
            }
        }
        return false
    }
};

const guess = () => {
    const isCorrect = isMarkerInsidePolygon()
    hintState.value = false
    if (isCorrect) {
        if (currentIndex.value == (places.value.length - 1)) {
            gameState.value = "won"
        } else {
            gameState.value = "correctRound"
        }
    } else {
        gameState.value = "lose"
    }
}


const getHint = () => {hintState.value = true}
const hint = computed(() => currentPlace.value.properties.population)
const score = computed(() => currentIndex.value)


</script>

<template>
    <div class="flex flex-col justify-between h-full">
        <Score :score="score" />
        <svg class="relative h-full" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
            <image :xlink:href="currentPlace.properties.flag" width="100%" />
        </svg>
        <Hint :hint="hint" />
        <button class="button" @click="getHint()">Hint</button>
        <button class="button" @click="guess()">Guess</button>
    </div>
</template>
