import { writable } from "svelte/store";

import type { Trads } from "../utils/trads";

export const trads = writable<Trads>();
