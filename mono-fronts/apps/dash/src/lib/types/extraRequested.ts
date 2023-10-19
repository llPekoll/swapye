export interface ExtraReqWordings {
    value: "";
    lang: "";
}
export interface ExtraRequested {
    key: "";
    kind: "";
    wordings: ExtraReqWordings[];
}
export interface ExtraReqReturn {
    extraElements: ExtraRequested[];
    langs: string[];
}