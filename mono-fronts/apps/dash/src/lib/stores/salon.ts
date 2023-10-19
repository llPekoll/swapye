import { writable } from "svelte/store";
import type { Salon } from "$lib/types/salon";

export const salon = writable<Salon>({
    fullScreenBtn: false,
    restartBtn: false,
    automaticRestart: false,
    automaticRestartCounterValue: 0,
    soundOveride: false
});