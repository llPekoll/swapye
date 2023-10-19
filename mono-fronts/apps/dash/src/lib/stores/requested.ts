import { writable } from "svelte/store";
import type { Requested } from "$lib/types";

export const requested = writable<Requested>({
    requestName: false,
    requestTel: false,
    requestAddress: false,
    isAlwaysWinner: false,
    canReplay: false,
    canReplayToday: false,
    emailCheck: false,
    emailCheckOverride: false,
});
