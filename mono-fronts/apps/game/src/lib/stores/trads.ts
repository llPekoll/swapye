import { writable } from "svelte/store";
import type { Game } from "$lib/interfaces";

export const trads = writable<Game>();