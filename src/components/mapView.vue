<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker, LGeoJson } from "@vue-leaflet/vue-leaflet";
import { ref, computed } from "vue";
import { CRS, latLng } from "leaflet";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from '../stores/gameState';

const gameStateStore = useGameStateStore()
const { places, currentIndex, gameState, markerPosition } = storeToRefs(gameStateStore);

const map = ref();
const crs = CRS.Base;
const placePolygon = ref(null)

function initMap(mapObj) {
    map.value = mapObj;
    map.value.doubleClickZoom.disable();
    map.value.addEventListener('click', function (ev) {
        let newLng = (ev.latlng.lng + 180)
        newLng = newLng - Math.floor(newLng / 360) * 360
        newLng -= 180
        const newLat = ev.latlng.lat
        markerPosition.value = latLng(newLat, newLng)
        map.value.setView(latLng(newLat, newLng))
    });
}

const currentPlace = computed(() => places.value[currentIndex.value])

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
    <l-map id="root" @ready="initMap" :crs="crs" :zoom="2" :center="[0, 0]" :options="{ attributionControl: false }"
        :min-zoom="1" :max-zoom="18">
        <l-marker :lat-lng="markerPosition" />
        <l-tile-layer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base" name="OpenStreetMap" />
        <l-geo-json v-if="currentPlace" ref="placePolygon" :geojson="currentPlace" :visible="polyVisible"
            :optionsStyle="() => { return { 'color': polyColor, 'fillColor': polyColor } }" />
    </l-map>
</template>

<style>
.leaflet-container {
    background: rgb(170 211 223);
    outline: 0;
}
</style>