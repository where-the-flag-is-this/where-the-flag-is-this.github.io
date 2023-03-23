<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker, LGeoJson } from "@vue-leaflet/vue-leaflet";
import { ref, computed } from "vue";
import { CRS, latLng } from "leaflet";
import allPlaces from "./assets/allPlaces.json"

const zoom = ref(2)
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
// {
//   "type": "Feature",
//   "properties": { "party": "Republican" },
//   "geometry": {
//     "type": "Polygon",
//     "coordinates": [[
//       [-104.05, 48.99],
//       [-97.22, 48.98],
//       [-96.58, 45.94],
//       [-104.03, 45.94]
//     ]]
//   }
// }

// allPlaces["features"][0]
function pointInPolygon(x: number, y: number, polyPoints) {
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
  if (isCorrect) {
    currentIndex.value++
  } else {
    currentIndex.value = 0
  }
}

</script>

<template>
  <div class="w-screen h-screen bg-green-400 flex">
    <div class="w-4/5 h-full overflow-x-hidden">
      <l-map id="root" @ready="initMap" :crs="crs" v-model="zoom" v-model:zoom="zoom" :center="[0, 0]"
        :options="{ attributionControl: false }" :min-zoom="1" :max-zoom="18">
        <l-marker :lat-lng="markerPosition" />
        <l-tile-layer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"
          name="OpenStreetMap"></l-tile-layer>
        <l-geo-json ref="placePolygon" :geojson="countryGeoJson" :visible="true" />
      </l-map>
    </div>
    <div class="w-1/5 h-full bg-slate-200 overflow-x-hidden">
      <div class="flex flex-col justify-end h-full">
        <p>Score: {{ currentIndex }}</p>
        <p>Where is {{ countryGeoJson.properties.ADMIN }}</p>
        <button class="bg-green-500 rounded-full m-2 text-3xl p-2" @click="guess()">Guess</button>
      </div>
    </div>
  </div>
</template>
