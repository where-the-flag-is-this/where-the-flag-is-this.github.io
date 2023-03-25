<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker, LGeoJson } from "@vue-leaflet/vue-leaflet";
import { ref, computed } from "vue";
import { CRS, latLng } from "leaflet";
import allPlaces from "./assets/allPlaces.json"

function shuffleArray(array: Array<any>) {
  for (var i = array.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
}

shuffleArray(allPlaces["features"])
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

const countryGeoJson = computed(() => allPlaces["features"][currentIndex.value])

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
  const isCorrect = isMarkerInsidePolygon()
  console.log(isCorrect)
  if (gameState.value === "ongoingRound") {
    if (isCorrect) {
      gameState.value = "correctRound"

    } else {
      gameState.value = "lose"
    }
  } else if (gameState.value === "correctRound") {
    currentIndex.value++
    gameState.value = "ongoingRound"
  } else {
    gameState.value = "ongoingRound"
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
          :optionsStyle="{ 'color': polyColor, 'fillColor': polyColor }" />
      </l-map>
    </div>
    <div class="w-1/5 h-full bg-slate-200 overflow-x-hidden">
      <div class="flex flex-col justify-between h-full">
        <p>Score: {{ currentIndex }}</p>
        <svg width="100%" height="90">
          <image :xlink:href="countryGeoJson.properties.FLAG_URL" width="100%" height="90" />
        </svg>
        <button class="bg-green-500 rounded-full m-2 text-3xl p-2" @click="guess()">{{ buttonText }}</button>
      </div>
    </div>
  </div>
</template>
