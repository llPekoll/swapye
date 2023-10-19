import { writable } from "svelte/store";
import type { Price } from "$lib/types";

interface PricesStore {
    prices: Price[];
    langs: string[];
    enableQr: boolean;

}
export const prices = writable<PricesStore>();
