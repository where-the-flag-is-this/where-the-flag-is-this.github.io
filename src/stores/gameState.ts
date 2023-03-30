import { defineStore } from "pinia";
import { ref, Ref } from "vue";
import { Place } from "../types/Place";
import allPlaces from "../assets/allPlaces.json"

export const useGameStateStore = defineStore('gameState', () => {
    const places: Ref<Place[]> = ref(allPlaces.features); // ref = state
    const currentIndex: Ref<number> = ref(0)

    return {
        places, currentIndex
    }
})