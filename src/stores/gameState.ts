import { defineStore } from "pinia";
import { computed, ref, Ref } from "vue";
import { Place } from "../types/Place";
import allPlaces from "../assets/allPlaces.json"
import { LatLng, latLng } from "leaflet";

export const useGameStateStore = defineStore('gameState', () => {
    const places: Ref<Place[]> = ref(allPlaces.features); // ref = state
    const currentIndex: Ref<number> = ref(0)
    const gameState: Ref<"newGame" | "won" | "lose" | "correctRound" | "ongoingRound"> = ref("newGame")
    const markerPosition: Ref<LatLng> = ref(latLng(0, 0))

    const currentPlace = computed(() => places.value[currentIndex.value])

    const shuffleAllPlaces = () => {
        let _newFeatures = places.value
        _newFeatures.sort(() => Math.random() - 0.5)
        places.value = _newFeatures
    }

    return {
        places, currentIndex, gameState, shuffleAllPlaces, markerPosition, currentPlace
    }
})