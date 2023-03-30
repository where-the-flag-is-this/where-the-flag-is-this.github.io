<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { ref, computed } from "vue";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from './stores/gameState';
import MapView from "./components/mapView.vue"

const gameStateStore = useGameStateStore()
const { places, currentIndex, gameState, markerPosition } = storeToRefs(gameStateStore);
const { shuffleAllPlaces } = gameStateStore

shuffleAllPlaces()

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
  if (gameState.value === "ongoingRound") {
    const isCorrect = isMarkerInsidePolygon()
    if (isCorrect) {
      if (currentIndex.value == (places.value.length - 1)) {
        gameState.value = "won"
      } else {
        gameState.value = "correctRound"
      }
    } else {
      gameState.value = "lose"
    }
  } else if (gameState.value === "correctRound") {
    currentIndex.value++
    gameState.value = "ongoingRound"
  } else {
    gameState.value = "ongoingRound"
    shuffleAllPlaces()
    currentIndex.value = 0
  }
}

const buttonText = computed(() => {
  if (["won", "lose", "none"].indexOf(gameState.value) > -1) {
    return "Start Game"
  }
  if (gameState.value === "correctRound") {
    return "Next round"
  }
  if (gameState.value === "ongoingRound") {
    return "Guess"
  }
  return "Unknown gamestate: " + gameState.value
})

const score = computed(() => {
  if (["won", "correctRound"].indexOf(gameState.value) > -1) {
    return currentIndex.value + 1
  }
  return currentIndex.value

})

</script>

<template>
  <div class="w-screen h-screen bg-green-400 flex">
    <div class="w-4/5 h-full overflow-x-hidden">
      <MapView />
    </div>
    <div class="w-1/5 h-full bg-slate-200 overflow-x-hidden">
      <div class="flex flex-col justify-between h-full">
        <div class="flex flex-col pb-8">
          <h1 class="w-full flex justify-center text-4xl">Score</h1>
          <p class="w-full flex justify-center text-4xl">{{ score }}</p>
        </div>
        <svg v-if="gameState === 'ongoingRound'" class="relative h-full" viewBox="0 0 100 100"
          preserveAspectRatio="xMidYMid meet">
          <image :xlink:href="currentPlace.properties.flag" width="100%" />
        </svg>
        <div v-if="gameState === 'won'">
          YOU WON!
        </div>
        <div v-if="gameState === 'correctRound'">
          Correct! It was <b>{{ currentPlace.properties.ADMIN }}</b>
        </div>
        <div v-if="gameState === 'lose'">
          Sorry that is wrong, the correct answer was <b>{{ currentPlace.properties.ADMIN }}</b>.
          Try again
        </div>
        <button class="bg-green-500 rounded-full m-2 text-3xl p-2" @click="guess()">{{ buttonText }}</button>
      </div>
    </div>
  </div>
</template>
