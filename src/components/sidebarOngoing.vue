<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { computed } from "vue";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from '../stores/gameState';
import Score from "./score.vue"

const gameStateStore = useGameStateStore()
const { places, currentIndex, gameState, markerPosition } = storeToRefs(gameStateStore);


const currentPlace = computed(() => places.value[currentIndex.value])

function distanceToPolygon(x: number, y: number, polyPoints: Array<Array<number>>) {
    let minDist = Number.MAX_VALUE;
    for (let i = 0; i < polyPoints.length; i++) {
        // Point 2 is the next in line, wrapping around to the first point
        const x1 = polyPoints[i][0], y1 = polyPoints[i][1];
        const nextIdx = (i + 1) % polyPoints.length;
        const x2 = polyPoints[nextIdx][0], y2 = polyPoints[nextIdx][1];

        const base = Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
        const heightSquare = Math.abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / base

        if (heightSquare < minDist) {
            minDist = heightSquare
        }
    }
    // By only taking the square root at the end, we avoid computing it multiple times
    return minDist
}

function pointInPolygon(x: number, y: number, polyPoints: Array<Array<number>>) {
    let inside = false;
    for (let i = 0, j = polyPoints.length - 1; i < polyPoints.length; j = i++) {
        const xi = polyPoints[i][0], yi = polyPoints[i][1];
        const xj = polyPoints[j][0], yj = polyPoints[j][1];
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

function distanceMarkerToPolygon() {
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
    }
};

const guess = () => {
    const isCorrect = isMarkerInsidePolygon()
    if (isCorrect) {
        if (currentIndex.value == (places.value.length - 1)) {
            gameState.value = "won"
        } else {
            gameState.value = "correctRound"
        }
    } else {
        console.log("Distance to polygon:", distanceMarkerToPolygon())
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
