import { writable } from 'svelte/store';
import type { PriceTrad } from '$lib/interfaces';

export const priceTrad = writable<PriceTrad>({
    img: '',
    name: ''
});
