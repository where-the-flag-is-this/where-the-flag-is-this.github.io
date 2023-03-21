<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";
import { ref } from "vue";
import customCRS from "./customCRS";

const zoom = ref(2)
const map = ref();
const crs = customCRS;
function initMap(mapObj) {
  map.value = mapObj;
}
</script>

<template>
  <div style="height:600px; width:800px">
    <l-map id="root" @ready="initMap" :crs="crs" class="rounded-b-lg" v-model="zoom" v-model:zoom="zoom"
      :center="[47.41322, -1.219482]" :options="{ attributionControl: false }" :min-zoom="1" :max-zoom="18">
      <l-tile-layer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"
        name="OpenStreetMap"></l-tile-layer>
    </l-map>
  </div>
</template>
