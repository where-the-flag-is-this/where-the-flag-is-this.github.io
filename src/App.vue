<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker, LGeoJson } from "@vue-leaflet/vue-leaflet";
import { ref, computed } from "vue";
import { CRS, latLng } from "leaflet";
import _allPlaces from "./assets/allPlaces.json"

const allPlaces = ref(_allPlaces)
const shuffleAllPlaces = () => {
  let _newFeatures = allPlaces.value.features
  _newFeatures.sort(() => Math.random() - 0.5)
  allPlaces.value.features = _newFeatures
}

shuffleAllPlaces()
const gameState = ref<"none" | "won" | "lose" | "correctRound" | "ongoingRound">("none")
const map = ref();
const crs = CRS.Base;
const markerPosition = ref(latLng(0, 0))
const currentIndex = ref(0)
const placePolygon = ref(null)

function initMap(mapObj) {
  map.value = mapObj;
  map.value.doubleClickZoom.disable();
  map.value.addEventListener('click', function (ev) {
    markerPosition.value = latLng(ev.latlng.lat, ev.latlng.lng)
  });
}

const countryGeoJson = computed(() => allPlaces.value["features"][currentIndex.value])

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
  if (countryGeoJson.value.geometry.type == "Polygon") {
    const polyPoints = countryGeoJson.value.geometry.coordinates[0];
    return pointInPolygon(x, y, polyPoints)
  } else if (countryGeoJson.value.geometry.type == "MultiPolygon") {
    for (var i = 0; i < countryGeoJson.value.geometry.coordinates.length; i++) {
      const polyPoints = countryGeoJson.value.geometry.coordinates[i][0];
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
      if (currentIndex.value == (allPlaces.value.features.length - 1)) {
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

const polyVisible = computed(() => {
  if (["won", "lose", "correctRound"].indexOf(gameState.value) > -1)
    return true
  return false
})
const polyColor = computed(() => {
  if (["won", "correctRound"].indexOf(gameState.value) > -1) {
    return "#00FF00"
  } else if (["lose"].indexOf(gameState.value) > -1) {
    return "#FF0000"
  }
  return "#0000FF"
})
</script>

<template>
  <div class="w-screen h-screen bg-green-400 flex">
    <div class="w-4/5 h-full overflow-x-hidden">
      <l-map id="root" @ready="initMap" :crs="crs" :zoom="2" :center="[0, 0]" :options="{ attributionControl: false }"
        :min-zoom="1" :max-zoom="18">
        <l-marker :lat-lng="markerPosition" />
        <l-tile-layer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base" name="OpenStreetMap"
          :no-wrap="true" />
        <l-geo-json ref="placePolygon" :geojson="countryGeoJson" :visible="polyVisible"
          :optionsStyle="() => { return { 'color': polyColor, 'fillColor': polyColor } }" />
      </l-map>
    </div>
    <div class="w-1/5 h-full bg-slate-200 overflow-x-hidden">
      <div class="flex flex-col justify-between h-full">
        <div class="flex flex-col">
          <h1 class="w-full flex justify-center text-4xl">Score</h1>
          <p class="w-full flex justify-center text-4xl">{{ score }}</p>
        </div>
        <svg v-if="gameState === 'ongoingRound'" class="relative" viewBox="0 0 100 100">
          <!--</image>:xlink:href="countryGeoJson.properties.FLAG_URL" -->
          <!--https://upload.wikimedia.org/wikipedia/commons/9/9b/Flag_of_Nepal.svg -->
          <!--https://upload.wikimedia.org/wikipedia/commons/6/6f/Flag_of_the_Central_African_Republic.svg" -->
          <image :xlink:href="countryGeoJson.properties.FLAG_URL" class="absolute" width="100%" height="100%" />
        </svg>
        <div v-if="gameState === 'won'">
          YOU WON!
        </div>
        <div v-if="gameState === 'lose'">
          Sorry that is wrong, the correct answer was {{ countryGeoJson.properties.ADMIN }}.
          Try again
        </div>
        <button class="bg-green-500 rounded-full m-2 text-3xl p-2" @click="guess()">{{ buttonText }}</button>
      </div>
    </div>
  </div>
</template>
