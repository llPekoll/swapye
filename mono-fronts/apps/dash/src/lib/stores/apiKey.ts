import { writable } from "svelte/store";
import type { Api } from "$lib/types";

export const apiKey = writable<Api>({
    provider: '',
    apikey: '',
    apipass: '',
    email: '',
    display_name: '',
    providers: []

});