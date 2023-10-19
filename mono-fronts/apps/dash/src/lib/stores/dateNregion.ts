import { writable } from "svelte/store";
import type { DateNRegion } from "$lib/types";

export const dateNregion = writable<DateNRegion>();