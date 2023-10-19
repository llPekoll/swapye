import { writable } from "svelte/store";
import type { Winner } from "$lib/interfaces";

export const winner = writable<Winner>({
    state: 'won',
    dayNumber: 0
});