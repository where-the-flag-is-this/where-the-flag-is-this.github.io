<script setup lang="ts">
import "leaflet/dist/leaflet.css";
import { computed, ref, watch } from "vue";

import { storeToRefs } from 'pinia';
import { useGameStateStore } from '../stores/gameState';
import allPlaces from "../assets/allPlaces.json"
import Score from "./score.vue"

const gameStateStore = useGameStateStore()
const { currentIndex, gameState, places } = storeToRefs(gameStateStore);
const { shuffleAllPlaces } = gameStateStore
const includeAfrica = ref(true)
const includeAsia = ref(true)
const includeNorthAmerica = ref(true)
const includeSouthAmerica = ref(true)
const includeEurope = ref(true)
const includeOceania = ref(true)

const startGame = () => {
    gameState.value = "ongoingRound"
    shuffleAllPlaces()
    currentIndex.value = 0
}

const score = computed(() => currentIndex.value)

const filterPlaces = () => {
    console.log("Filter")
    places.value = allPlaces.features.filter(place => {

        if (includeAsia.value && place.properties.continents.indexOf("Asia") > -1) {
            return true
        }
        if (includeAfrica.value && place.properties.continents.indexOf("Africa") > -1) {
            return true
        }
        if (includeEurope.value && place.properties.continents.indexOf("Europe") > -1) {
            return true
        }
        if (includeNorthAmerica.value && place.properties.continents.indexOf("North America") > -1) {
            return true
        }
        if (includeSouthAmerica.value && place.properties.continents.indexOf("South America") > -1) {
            return true
        }
        if (includeOceania.value && place.properties.continents.indexOf("Insular Oceania") > -1) {
            return true
        }
    })
}
watch([includeAfrica, includeAsia,
    includeNorthAmerica,
    includeSouthAmerica,
    includeEurope,
    includeOceania], () => {
        filterPlaces()
    })

filterPlaces()
</script>

<template>
    <div class="flex flex-col justify-between h-full">
        <Score :score="score" />
        <div>
            <p>
                You will get a flag of a place. Guess where it is on the map an hit 'Guess'.
                The locations are from WikiData and linked to active jurisdiction not claims!
            </p>
        </div>
        <div class="flex flex-col">
            <h1>What continents needs to be included</h1>
            <div>
                <input class="mx-2" type="checkbox" id="checkbox" v-model="includeAfrica" />
                <label>Africa</label>
            </div>
            <div>
                <input class="mx-2" type="checkbox" id="checkbox" v-model="includeAsia" />
                <label>Asia</label>
            </div>
            <div>
                <input class="mx-2" type="checkbox" id="checkbox" v-model="includeNorthAmerica" />
                <label>NorthAmerica</label>
            </div>
            <div>
                <input class="mx-2" type="checkbox" id="checkbox" v-model="includeSouthAmerica" />
                <label>SouthAmerica</label>
            </div>
            <div>
                <input class="mx-2" type="checkbox" id="checkbox" v-model="includeEurope" />
                <label>Europe</label>
            </div>
            <div>
                <input class="mx-2" type="checkbox" id="checkbox" v-model="includeOceania" />
                <label>Oceania</label>
            </div>
        </div>
        <button :disabled="places.length == 0" class="button" @click="startGame()">Start
            Game</button>
    </div>
</template>
