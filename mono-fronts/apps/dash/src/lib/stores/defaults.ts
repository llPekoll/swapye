import { writable } from "svelte/store";
import type { Defaults } from "$lib/types";

export const defaults = writable<Defaults>({
    email_check: '',
    logo: '',
    music: '',

});