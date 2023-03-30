import { defineStore } from "pinia";
import { ref, Ref } from "vue";
import { Place } from "../types/Place";
import allPlaces from "../assets/allPlaces.json"
import { LatLng, latLng } from "leaflet";

export const useGameStateStore = defineStore('gameState', () => {
    const places: Ref<Place[]> = ref(allPlaces.features); // ref = state
    const currentIndex: Ref<number> = ref(0)
    const gameState: Ref<"none" | "won" | "lose" | "correctRound" | "ongoingRound"> = ref("none")
    const markerPosition: Ref<LatLng> = ref(latLng(0, 0))

    const shuffleAllPlaces = () => {
        let _newFeatures = places.value
        _newFeatures.sort(() => Math.random() - 0.5)
        places.value = _newFeatures
    }

    return {
        places, currentIndex, gameState, shuffleAllPlaces, markerPosition
    }
})