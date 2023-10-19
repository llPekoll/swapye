import { writable } from "svelte/store";
import { winner } from "./winner";
import { game } from "./game";
import { priceTrad } from "./priceTrad";

const formSubmited = writable(false);


export { game, winner, formSubmited, priceTrad };
