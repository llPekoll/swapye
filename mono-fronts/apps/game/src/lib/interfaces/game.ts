import type { ExtraRequested } from "./extraRequested";

export interface Game {
    emblem: string,
    name: string,
    logo: string,
    gameTypeIdRef: number,
    skinIdRef: number,

    emailCheck: boolean,

    displayFullScreen: boolean,
    fullscreenBtn: boolean,

    formColor: string,

    dryRun: boolean,
    extraRequested: ExtraRequested[],
    // BG
    bgIngame: string,
    music?: string,
    // before Form (Intro)
    formPortrait: string,
    formLandscape: string,
    // restart
    restartBtn: boolean,
    automaticRestart: boolean,
    automaticRestartCounterValue: number,
    // Form
    requestName: boolean,
    requestTel: boolean,
    requestAddress: boolean,
    // calendar
    winnerDay?: string,
    numberOfDays?: number[],
}
