<script setup lang="ts">
import "leaflet/dist/leaflet.css";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from './stores/gameState';
import MapView from "./components/mapView.vue"
import sidebarNewGame from "./components/sidebarNewGame.vue"
import sidebarOngoing from "./components/sidebarOngoing.vue"
import sidebarCorrectRound from "./components/sidebarCorrectRound.vue"
import sidebarLose from "./components/sidebarLose.vue"
import sidebarWon from "./components/sidebarWon.vue"

const gameStateStore = useGameStateStore()
const { gameState } = storeToRefs(gameStateStore);


</script>

<template>
  <div class="w-screen h-screen bg-gray-300 flex">
    <div class="w-4/5 h-full overflow-x-hidden">
      <MapView />
    </div>
    <div class="w-1/5 h-full bg-slate-200 overflow-x-hidden">
      <sidebarNewGame v-if="gameState === 'newGame'" />
      <sidebarOngoing v-if="gameState === 'ongoingRound'" />
      <sidebarWon v-if="gameState === 'won'" />
      <sidebarCorrectRound v-if="gameState === 'correctRound'" />
      <sidebarLose v-if="gameState === 'lose'" />
    </div>
  </div>
</template>
