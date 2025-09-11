<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { computed } from "vue";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from '../stores/gameState';
import { distanceToPolygon, pointInPolygon } from '../utils/geometryUtils';
import Score from "./score.vue"

const gameStateStore = useGameStateStore()
const { places, currentIndex, gameState, markerPosition } = storeToRefs(gameStateStore);


const currentPlace = computed(() => places.value[currentIndex.value])

function isMarkerInsidePolygon(): boolean {
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
    } else {
        throw new Error("Not implemented: Unsupported geometry type");
    }
};

function distanceMarkerToPolygon(): number {
    const x = markerPosition.value.lng, y = markerPosition.value.lat;
    console.log("Marker position:", x, y)
    console.log("Current place:", currentPlace.value)
    if (currentPlace.value.geometry.type == "Polygon") {
        const polyPoints = currentPlace.value.geometry.coordinates[0];
        return distanceToPolygon(x, y, polyPoints)
    } else if (currentPlace.value.geometry.type == "MultiPolygon") {
        let minDist = Number.MAX_VALUE;
        for (var i = 0; i < currentPlace.value.geometry.coordinates.length; i++) {
            const polyPoints = currentPlace.value.geometry.coordinates[i][0];
            const newDist = distanceToPolygon(x, y, polyPoints)
            if (newDist < minDist) {
                minDist = newDist
            }
        }
        return minDist
    } else {
        throw new Error("Not implemented: Unsupported geometry type");
    }
};

const guess = () => {
    let isCorrect = isMarkerInsidePolygon()
    // Allow a small margin of error (0.1 degrees) for guessing
    if (!isCorrect) {
        const distanceError: number = distanceMarkerToPolygon()
        if(distanceError < 0.1) {
            isCorrect = true
        }
    }
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

const score = computed(() => currentIndex.value)

</script>

<template>
    <div class="flex flex-col justify-between h-full">
        <Score :score="score" />
        <svg class="relative h-full" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
            <image :xlink:href="currentPlace.properties.flag" width="100%" />
        </svg>
        <button class="button" @click="guess()">Guess</button>
    </div>
</template>
