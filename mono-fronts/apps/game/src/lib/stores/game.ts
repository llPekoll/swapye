import { writable } from "svelte/store";
import type { Game } from "$lib/interfaces";

export const game = writable<Game>({
    emblem: '',
    name: '',
    logo: '',
    gameTypeIdRef: 1,
    skinIdRef: 1,

    emailCheck: false,

    displayFullScreen: false,
    fullscreenBtn: false,

    formColor: '',

    dryRun: false,
    extraRequested: [],

    bgIngame: '',
    music: '',

    formPortrait: '',
    formLandscape: '',

    restartBtn: false,
    automaticRestart: false,
    automaticRestartCounterValue: 1,

    requestName: false,
    requestTel: false,
    requestAddress: false,

    winnerDay: '',
    numberOfDays: [0],
});