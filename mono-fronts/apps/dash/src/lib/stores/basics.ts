import { writable } from "svelte/store";
import type { Basics } from "$lib/types";

export const basics = writable<Basics>({
    name: "",
    skin: 0,
    type: 0,
    idSkin: 0,
    idType: 0,
    bgIngame: ""

});
