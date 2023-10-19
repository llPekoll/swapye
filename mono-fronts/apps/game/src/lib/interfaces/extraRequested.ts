export interface ExtraReqWordings {
    value: string; // not sure about this one
    wording: string;
    lang: string;
}
export interface ExtraRequested {
    key: string;
    kind: string;
    wordings: ExtraReqWordings[];
}
export interface ExtraReqReturn {
    extraElements: ExtraRequested[];
    langs: string[];
}