import { defineStore } from "pinia";
import { computed, ref, Ref } from "vue";
import { Place } from "../types/Place";
import allPlaces from "../assets/allPlaces.json"
import { LatLng, latLng } from "leaflet";

function shuffleArray(array: Array<any>) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1)); // Generate a random index between 0 and i
        // Swap elements at i and j
        [array[i], array[j]] = [array[j], array[i]];
    }
}

export const useGameStateStore = defineStore('gameState', () => {
    const places: Ref<Place[]> = ref(allPlaces.features); // ref = state
    const currentIndex: Ref<number> = ref(0)
    const gameState: Ref<"newGame" | "won" | "lose" | "correctRound" | "ongoingRound"> = ref("newGame")
    const markerPosition: Ref<LatLng> = ref(latLng(0, 0))

    const currentPlace = computed(() => places.value[currentIndex.value])

    const shuffleAllPlaces = () => {
        shuffleArray(places.value)
    }

    return {
        places, currentIndex, gameState, shuffleAllPlaces, markerPosition, currentPlace
    }
})