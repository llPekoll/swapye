import { writable } from "svelte/store";
import type { ExtraReqReturn } from "$lib/types";

export const extraReqReturn = writable<ExtraReqReturn>({
    extraElements: [],
    langs: []
});
