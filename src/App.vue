<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
import { ref } from "vue";
import { CRS, latLng } from "leaflet";

const zoom = ref(2)
const map = ref();
const crs = CRS.Base;
const markerPosition = ref(latLng(0, 0))
function initMap(mapObj) {
  map.value = mapObj;
  map.value.doubleClickZoom.disable();
  map.value.addEventListener('click', function (ev) {
    markerPosition.value = latLng(ev.latlng.lat, ev.latlng.lng)
  });
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
      </l-map>
    </div>
    <div class="w-1/5 h-full bg-slate-200 overflow-x-hidden">

    </div>
  </div>
</template>
